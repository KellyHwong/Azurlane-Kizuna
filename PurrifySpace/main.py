#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-27 17:18:48
# @Author  : Kelly Hwong (https://github.com/KellyHwong)
# @Link    : http://example.org
# @Version : $Id$

import os
import copy

GAIN_FACTOR = 2

# 把数据载入空间里
class DataSpace(object):
    """docstring for DataSpace"""
    def __init__(self, data:list, score=0):
        super(DataSpace, self).__init__()
        self.data = copy.deepcopy(data)
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.score = score

    def show(self):
        for row in self.data:
            for col in row:
                print(str(col), end="")
                print(' ', end="")
            print("\n", end="")

    def update_point(self, x, y):
        if self.data[x][y] == 1:
            self.data[x][y] = 0
            self.score -= 1 * GAIN_FACTOR
        elif self.data[x][y] == 0:
            self.data[x][y] = 1
            self.score += 1 * GAIN_FACTOR

    def calulate_point(self, x, y):
        if self.data[x][y] == 1:
            # self.data[x][y] = 0
            return -1 * GAIN_FACTOR
        elif self.data[x][y] == 0:
            # self.data[x][y] = 1
            return 1 * GAIN_FACTOR

    # 输入坐标 x, y ，改变这个位置的黑白状态
    def update_data(self, x, y):
        coordinates = [
            (x-1,y-1), (x,y-1), (x+1,y-1),
            (x-1,y), (x,y), (x+1,y),
            (x-1,y+1), (x,y+1), (x+1,y+1)
        ]
        for x, y in coordinates:
            if x in range(self.height) and y in range(self.width):
                self.update_point(x, y)

    def calulate_step(self, x, y):
        updated_score = 0
        coordinates = [
            (x-1,y-1), (x,y-1), (x+1,y-1),
            (x-1,y), (x,y), (x+1,y),
            (x-1,y+1), (x,y+1), (x+1,y+1)
        ]
        for x, y in coordinates:
            if x in range(self.height) and y in range(self.width):
                updated_score += self.calulate_point(x, y)
        return updated_score


class UIInterface(object):
    """docstring for UIInterface"""
    def __init__(self, arg):
        super(UIInterface, self).__init__()
        self.arg = arg

class Algorithm(object):
    """docstring for Algorithm"""
    def __init__(self, dataSpace: DataSpace):
        super(Algorithm, self).__init__()
        self.dataSpace = dataSpace
        self.valid_steps = []
        for x in range(self.dataSpace.height):
            for y in range(self.dataSpace.width):
                self.valid_steps.append((x, y))

    def step_with_score(self):
        step_with_score = []
        for step in self.valid_steps:
            score = self.dataSpace.calulate_step(step[0], step[1])
            step_with_score.append((score, step))
        return step_with_score

    # 查询最大值问题

def main():
    # 数据录入工具
    # 万能的CSV/Excel来做
    # 或者做一个GUI
    data = [
    [1,0,0,1,0,0,1,1,1],
    [1,0,1,0,0,0,0,1,0],
    [1,1,0,0,0,0,0,1,0],
    [1,0,1,0,0,0,0,1,0],
    [1,0,0,1,0,0,1,1,1],
    [0,0,0,0,0,0,0,0,0],
    ]
    dataSpace = DataSpace(data)
    # input_text = input()
    # x, y = input_text.split()
    dataSpace.show()
    # dataSpace.update_data_space(3-1,5-1)
    print("========current score    ========")
    print(dataSpace.score)
    print("========current dataspace========")
    dataSpace.show()

    algo = Algorithm(dataSpace)
    given_steps = 3

    '''
    for i in range(given_steps):
        step_with_score = algo.step_with_score()
        # 找最大值
        max_score_steps = max(step_with_score, key=lambda x:x[0])
        max_score = max_score_steps[0]
        print("========max potential score========")
        print(max_score)
        tup = [(i, step_with_score[i]) for i in range(len(step_with_score))]
        best_step_i = [i for i, score_step in tup if score_step[0] == max_score]
        print("========best step list========")
        print(best_step_i)
        best_steps = [step_with_score[i] for i in best_step_i]
        print(best_steps)
        print("========choose the first best step========")
        step_score = step_with_score[best_step_i[0]]
        print(step_score)
        step = step_score[1]
        print(step)
        algo.dataSpace.update_data(step[0], step[1])
        print("========gained score========")
        print(max_score)
        print("========current score========")
        print(algo.dataSpace.score)
        if i != 2:
            print("========next step========")
    '''
    # '''
    # 暴力穷举法
    path = []
    score = []
    paths = []
    scores = []
    count = 0
    algo = Algorithm(DataSpace(data))
    valid_steps = algo.valid_steps
    for s0 in valid_steps:
        algo0 = Algorithm(DataSpace(data=data, score=0))
        algo0.dataSpace.update_data(s0[0], s0[1])
        path.append(s0)
        score.append(algo0.dataSpace.score)
        for s1 in valid_steps:
            algo1 = Algorithm(DataSpace(algo0.dataSpace.data, algo0.dataSpace.score))
            algo1.dataSpace.update_data(s1[0], s1[1])
            path.append(s1)
            score.append(algo1.dataSpace.score)
            for s2 in valid_steps:
                algo2 = Algorithm(DataSpace(algo1.dataSpace.data, algo1.dataSpace.score))
                algo2.dataSpace.update_data(s2[0], s2[1])
                path.append(s2)
                score.append(algo2.dataSpace.score)
                print(score, end="")
                print(path)
                # if (s0 == (2, 4)) and (s1 == (5, 1)) and (s2 == (5, 4)):
                    # print(score)
                    # print(path)
                    # input("等待。。。")
                scores.append(tuple(score))
                paths.append(tuple(path))
                del path[-1]
                del score[-1]
                count += 1
                print(count)
            del path[-1]
            del score[-1]
        del path[-1]
        del score[-1]

    # 找scores[i][2]中最大的
    max_score = max(scores, key=lambda item:item[-1])
    print("最大的分数是")
    print(max_score)
    print("重复的最大分数")
    _t = [(i, scores[i]) for i in range(len(scores))]
    max_scores_i = [i for i, _s in _t if _s[-1] == max_score[-1] ]
    max_scores = [scores[i] for i in max_scores_i]
    best_paths = [paths[i] for i in max_scores_i]
    print(max_scores)
    print(best_paths)
    # '''

if __name__ == '__main__':
    main()