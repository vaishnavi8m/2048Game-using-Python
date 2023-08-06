import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random

class Board:
  bg_color = {
  '2': '#63EBA4',
  '4': '#3FFF00',
  '8': '#209D5C',
  '16': '#77D150',
  '32': '#9BD483',
  '64': '#0F9200',
  '128': '#C2EFAF',
  '256': '#5C7B4F',
  '512': '#96FC96',
  '1024': '#98FE98',
  '2048': '#01BDA4',
}
  color = {
      '2': '#000000',
      '4': '#000000',
      '8': '#000000',
      '16': '#000000',
      '32': '#000000',
      '64': '#000000',
      '128': '#000000',
      '256': '#000000',
      '512': '#000000',
      '1024': '#000000',
      '2048': '#000000',
  }

  def __init__(self):
      self.n = 4
      self.window = Tk()
      self.window.title('Project 2048 Game')
      self.gameArea = Frame(self.window, bg='black')
      self.board = []
      self.gridCell = [[0] * 4 for i in range(4)]
      self.compress = False
      self.merge = False
      self.moved = False
      self.score = 0
      self.score_frame = Frame(self.window)

      for i in range(4):
          rows = []
          for j in range(4):
              l = Label(self.gameArea, text='', bg='azure4',
                        font=('arial', 22, 'bold'), width=5, height=3)
              l.grid(row=i, column=j, padx=7, pady=7)
              rows.append(l);
          self.board.append(rows)
      self.gameArea.grid(pady = (100,0))
     # self.gameArea.grid()

      #score system
      self.score_frame.place(relx= 0.5, y=45, anchor='center')
      score_lab = Label(self.score_frame, text='Score', font = ('arial', 24, 'bold')).grid(row=0)
      self.score_Label = Label(self.score_frame, text='0',font = ('arial', 24, 'bold') )
      self.score_Label.grid(row=1)

  def reverse(self):
      for ind in range(4):
          i = 0
          j = 3
          while (i < j):
              self.gridCell[ind][i], self.gridCell[ind][j] = self.gridCell[ind][j], self.gridCell[ind][i]
              i += 1
              j -= 1

  def transpose(self):
      self.gridCell = [list(t) for t in zip(*self.gridCell)]

  def compressGrid(self):
      self.compress = False
      temp = [[0] * 4 for i in range(4)]
      for i in range(4):
          cnt = 0
          for j in range(4):
              if self.gridCell[i][j] != 0:
                  temp[i][cnt] = self.gridCell[i][j]
                  if cnt != j:
                      self.compress = True
                  cnt += 1
      self.gridCell = temp

  def mergeGrid(self):
      self.merge = False
      for i in range(4):
          for j in range(4 - 1):
              if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                  self.gridCell[i][j] *= 2
                  self.gridCell[i][j + 1] = 0
                  self.score += self.gridCell[i][j]
                  self.merge = True

  def random_cell(self):
      cells = []
      for i in range(4):
          for j in range(4):
              if self.gridCell[i][j] == 0:
                  cells.append((i, j))
      curr = random.choice(cells)
      i = curr[0]
      j = curr[1]
      self.gridCell[i][j] = 2

  def can_merge(self):
      for i in range(4):
          for j in range(3):
              if self.gridCell[i][j] == self.gridCell[i][j + 1]:
                  return True

      for i in range(3):
          for j in range(4):
              if self.gridCell[i + 1][j] == self.gridCell[i][j]:
                  return True
      return False

  def paintGrid(self):
      for i in range(4):
          for j in range(4):
              if self.gridCell[i][j] == 0:
                  self.board[i][j].config(text='', bg='azure4')
              else:
                  self.board[i][j].config(text=str(self.gridCell[i][j]),
                                          bg=self.bg_color.get(str(self.gridCell[i][j])),
                                          fg=self.color.get(str(self.gridCell[i][j])))
      self.score_Label.config(text = self.score)

class Game:
  def __init__(self, gamepanel):
      self.gamepanel = gamepanel
      self.end = False
      self.won = False

  def start(self):
      self.gamepanel.random_cell()
      self.gamepanel.random_cell()
      self.gamepanel.paintGrid()
      self.gamepanel.window.bind('<Key>', self.link_keys)
      self.gamepanel.window.mainloop()

  def link_keys(self, event):
      if self.end or self.won:
          return

      self.gamepanel.compress = False
      self.gamepanel.merge = False
      self.gamepanel.moved = False

      presed_key = event.keysym

      if presed_key == 'Up':
          self.gamepanel.transpose()
          self.gamepanel.compressGrid()
          self.gamepanel.mergeGrid()
          self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
          self.gamepanel.compressGrid()
          self.gamepanel.transpose()

      elif presed_key == 'Down':
          self.gamepanel.transpose()
          self.gamepanel.reverse()
          self.gamepanel.compressGrid()
          self.gamepanel.mergeGrid()
          self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
          self.gamepanel.compressGrid()
          self.gamepanel.reverse()
          self.gamepanel.transpose()

      elif presed_key == 'Left':
          self.gamepanel.compressGrid()
          self.gamepanel.mergeGrid()
          self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
          self.gamepanel.compressGrid()

      elif presed_key == 'Right':
          self.gamepanel.reverse()
          self.gamepanel.compressGrid()
          self.gamepanel.mergeGrid()
          self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
          self.gamepanel.compressGrid()
          self.gamepanel.reverse()
      else:
          pass

      self.gamepanel.paintGrid()
      print(self.gamepanel.score)

      flag = 0
      for i in range(4):
          for j in range(4):
              if (self.gamepanel.gridCell[i][j] == 2048):
                  flag = 1
                  break

      if (flag == 1):  # found 2048
          self.won = True
          messagebox.showinfo('2048', message='You Wonnn!!')
          print("won")
          return

      for i in range(4):
          for j in range(4):
              if self.gamepanel.gridCell[i][j] == 0:
                  flag = 1
                  break

      if not (flag or self.gamepanel.can_merge()):
          self.end = True
          messagebox.showinfo('2048', 'Game Over!!!')
          print("Over")

      if self.gamepanel.moved:
          self.gamepanel.random_cell()

      self.gamepanel.paintGrid()

gamepanel = Board()
game2048 = Game(gamepanel)
game2048.start()




