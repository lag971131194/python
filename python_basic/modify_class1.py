from random import randint
import time


# 玩家
class Player:

    def __init__(self, stoneNumber):
        self.stoneNumber = stoneNumber  # 灵石数量
        self.warriors = {}  # 拥有的战士，包括弓箭兵和斧头兵


# 战士基类
class Warrior:

    def __init__(self, name, strength):
        self.name = name
        self.strength = strength
        self.maxStrength = strength

    def healing(self, stoneCount):
        if self.strength < self.maxStrength:
            self.strength += stoneCount
            if self.strength > self.maxStrength:
                self.strength = self.maxStrength


# 弓箭兵
class Archer(Warrior):
    typeName = '弓箭兵'
    price = 100

    def fightWithMonster(self, monster):
        if monster.typeName == '鹰妖':
            self.strength -= 20
        elif monster.typeName == '狼妖':
            self.strength -= 80


# 斧头兵
class Axeman(Warrior):
    typeName = '斧头兵'
    price = 120

    def fightWithMonster(self, monster):
        if monster.typeName == '鹰妖':
            self.strength -= 80
        elif monster.typeName == '狼妖':
            self.strength -= 20


# 妖怪基类
class Monster:
    pass


# 鹰妖
class Eagle(Monster):
    typeName = '鹰妖'


# 狼妖
class Wolf(Monster):
    typeName = '狼妖'


# 森林
class Forest:
    def __init__(self, monster):
        self.monster = monster


def main():
    print('''
***************************************
****           游戏开始             ****
***************************************
''')

    forest_num = 7
    forestList = []
    notification = '前方森林里的妖怪是：'

    for i in range(forest_num):
        typeName = randint(0, 1)
        if typeName == 0:
            forestList.append(Forest(Eagle()))
        else:
            forestList.append(Forest(Wolf()))

        notification += f'第{i + 1}座森林里面是 {forestList[i].monster.typeName}  '

    print(notification)
    time.sleep(10)  # 模拟等待10秒

    player = Player(1000)

    while True:
        print("请选择雇佣的战士类型：1. 弓箭兵 2. 斧头兵")
        choice = input()
        if choice == '1':
            num = int(input("请输入雇佣的数量："))
            for i in range(num):
                name = input("请输入战士的名字：")
                warrior = Archer(name)
                player.warriors[name] = warrior
                player.stoneNumber -= Archer.price
        elif choice == '2':
            num = int(input("请输入雇佣的数量："))
            for i in range(num):
                name = input("请输入战士的名字：")
                warrior = Axeman(name)
                player.warriors[name] = warrior
                player.stoneNumber -= Axeman.price
        else:
            print("输入错误，请重新输入！")
            continue
        break

    for i in range(forest_num):
        print(f"你现在进入了第{i + 1}座森林，请选择一个战士来消灭妖怪：")
        for name, warrior in player.warriors.items():
            print(f"{name}({warrior.strength}/{warrior.maxStrength})")
        chosen_warrior_name = input()
        chosen_warrior = player.warriors[chosen_warrior_name]
        chosen_warrior.fightWithMonster(forestList[i].monster)

        while chosen_warrior.strength <= 0:
            print("当前战士已牺牲，请选择其他战士继续战斗或退出游戏！")
            choice = input("1. 继续战斗 2. 退出游戏\n")
            if choice == '1':
                chosen_warrior_name = input("请选择其他战士：")
                chosen_warrior = player.warriors[chosen_warrior_name]
                chosen_warrior.fightWithMonster(forestList[i].monster)
            else:
                print("游戏结束！")
                return

        heal_choice = input("是否需要疗伤？1. 是 2. 否\n")
        if heal_choice == '1':
            heal_amount = int(input("请输入疗伤所需的灵石数量："))
            if heal_amount <= player.stoneNumber:
                chosen_warrior.healing(heal_amount)
                player.stoneNumber -= heal_amount
            else:
                print("灵石不足，无法疗伤！")

    print(f"恭喜你成功通过所有森林！剩余灵石：{player.stoneNumber}")


if __name__ == '__main__':
    main()
