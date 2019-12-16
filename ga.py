# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 20:41:50 2019

@author: Azumi Mamiya
"""

import matplotlib.pyplot as plt
import random
import copy

class SimpleGA:
    def __init__(self):
        self.N = 100# 染色体の数
        self.ITERATION = 100# 繰り返し
        self._initialize()
        self.average = []

    def _initialize(self):# 染色体を生成
        self.pool = [Chromosome() for i in range(self.N)]

    def _mutateAll(self):# 突然変異を起こす
        for i in range(self.N):
            self.pool[i].mutate()

    def _tournamentSelection(self):# トーナメント選択
        pool_next = []
        while len(pool_next) < self.N:
            offspring1 = copy.deepcopy(self.pool[random.randrange(self.N)])#ランダムで遺伝子をコピー
            offspring2 = copy.deepcopy(self.pool[random.randrange(self.N)])#ランダム遺伝子をでコピー
            if offspring1.getFittness() > offspring2.getFittness():#offspring1の適応度が高いとき
                pool_next.append(offspring1)#offspring1を追加
            else:#offspring2の適応度が高いとき
                pool_next.append(offspring2)#offspring2を追加
        self.pool = pool_next[:]

    def _rouletteSelection(self):# ルーレット選択
        # ルーレット選択の関数
        # ここを実装する
        pool_next = []
        total = 0
        for pool_i in self.pool:
            total += pool_i.getFittness()
        
        while (len(pool_next) < self.N):
            sum_fittness = 0
            p = random.random()
            for pool_i in self.pool:
                sum_fittness += pool_i.getFittness()
                if p <= sum_fittness/total:
                    pool_next.append(copy.deepcopy(pool_i))
                    break
        self.pool = pool_next[:]

    def _printStatus(self, iteration):# 
        print("generation\t" + str(iteration))# iteration: 繰り返し回数
        for c in self.pool:
            print("\t" + str(c))

    def _printAverage(self):
        # 適応度の平均値を計算する関数
        # ここを実装し，平均適応度の時間変化のグラフに利用する
        sum = 0
        for p in self.pool:
            sum += p.getFittness()
        average = sum/len(self.pool)
        #print("Average\t ", average)
        self.average.append(average)
    
    def create_fig(self):
        plt.plot(self.average, color='blue')
        plt.ylim(0,1)
        plt.ylabel('Average Fitness')
        plt.xlabel('Generation')
        
    def evolve(self):
        for i in range(self.ITERATION):
            #self._printStatus(i)
            self._printAverage()
            #self._tournamentSelection()
            self._rouletteSelection()
            self._mutateAll()
            
            self.create_fig()
            
class Chromosome:
    def __init__(self):
        self.LENGTH = 8# 長さ
        self.MUTATION_RATE = 0.05# 突然変異率
        self.gene = [random.randint(0,1) for i in range(self.LENGTH)]# 遺伝子

    def setGene(self, new_gene):
        self.gene = new_gene[:]

    def mutate(self):# 突然変異
        for i in range(self.LENGTH):
            if random.random() < self.MUTATION_RATE:
                self.gene[i] = 1 - self.gene[i]

    def getFittness(self):# 適応度の計算
        value = 0.
        for g in self.gene:
            value *= 2
            value += g
        result = value / (2 ** self.LENGTH - 1.0)
        # return result * result
        return result

    def __str__(self):
        result = ""
        for g in self.gene:
            result += str(g)
        result += "\t" + str(self.getFittness())
        return result

ga = SimpleGA()
ga.evolve()