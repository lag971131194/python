from random import randint
import time,sys

# 玩家
class Player:

    def __init__(self,stoneNumber):
        self.stoneNumber = stoneNumber # 灵石数量
        self.warriors = {}  # 拥有的战士，包括弓箭兵和斧头兵

# 战士
class Warrior:

    # 初始化参数是生命值
    def __init__(self, strength):
        self.strength = strength

    # 用灵石疗伤
    def healing(self, stoneCount):
        # 如果已经到达最大生命值，灵石不起作用，浪费了
        if self.strength == self.maxStrength:
            return

        self.strength += stoneCount

        # 不能超过最大生命值
        if self.strength > self.maxStrength:
            self.strength = self.maxStrength


# 弓箭兵 是 战士的子类
class Archer(Warrior):
    # 种类名称
    typeName = '弓箭兵'

    # 雇佣价 100灵石，属于静态属性
    price = 100

    # 最大生命值 ，属于静态属性
    maxStrength = 100


    # 初始化参数是生命值, 名字
    def __init__(self, name, strength = maxStrength):
        Warrior.__init__(self, strength)
        self.name = name

    # 和妖怪战斗
    def fightWithMonster(self,monster):
        if monster.typeName== '鹰妖':
            self.strength -= 20
        elif monster.typeName== '狼妖':
            self.strength -= 80
        else:
            print('未知类型的妖怪！！！')



# 斧头兵 是 战士的子类
class Axeman(Warrior):
    # 种类名称
    typeName = '斧头兵'

    # 雇佣价 120灵石
    price = 120

    # 最大生命值
    maxStrength = 120


    # 初始化参数是生命值, 名字
    def __init__(self, name, strength = maxStrength):
        Warrior.__init__(self, strength)
        self.name = name

    # 和妖怪战斗
    def fightWithMonster(self,monster):
        if monster.typeName== '鹰妖':
            self.strength -= 80
        elif monster.typeName== '狼妖':
            self.strength -= 20
        else:
            print('未知类型的妖怪！！！')

def hire_warriors(player):
    while True:
        # 初始化玩家，给玩家1000灵石
        player.stoneNumber = 1000
        # 显示菜单
        print(f'你现在拥有{player.stoneNumber}灵石，请选择要雇佣的战士类型的数量，有2种：\n\t弓箭兵（ hiring archer, cost 100 stones）\n\t斧头兵（ hiring axeman, cost 120 stones）\n')
        # 输入弓箭兵的数量
        num = get_valid_number_input(f'弓箭兵单价{Archer.price}灵石，请输入雇佣弓箭兵的数量：',player.stoneNumber,Archer.price)
        player.stoneNumber -= num * Archer.price
        hire_warrior_type(player, num, Archer)

        # 输入斧头兵的数量
        num = get_valid_number_input(f'斧头兵单价{Axeman.price}灵石，请输入雇佣斧头兵的数量：',player.stoneNumber,Axeman.price)
        player.stoneNumber -= num * Axeman.price
        hire_warrior_type(player, num, Axeman)
        break

def get_valid_number_input(prompt,available_stones,price):
    while True:
        try:
            num = int(input(prompt))
            if num < 0:
                print(f'输入有误，请输入非负整数,剩余灵石为：{available_stones}')
                time.sleep(1)
                continue
            if available_stones < num * price:
                print(f'你的灵石不够，无法雇佣！,请重新输入,剩余灵石为：{available_stones}')
                time.sleep(1)
                continue
            return num
        except ValueError:
            print(f'输入有误，请输入有效的整数,剩余灵石为：{available_stones}')
            time.sleep(1)

def hire_warrior_type(player, num, WarriorType):
    print(f'你一共要雇佣{num}个{WarriorType.typeName}，花费：{num * WarriorType.price}灵石，剩余：{player.stoneNumber}灵石')
    for i in range(num):
        while True:
            name = input(f'输入第{i+1}个{WarriorType.typeName}的名字：')
            if name in player.warriors:
                print(f'名字{name}重复，请重新输入')
                time.sleep(1)
                continue
            player.warriors[name] = WarriorType(name)
            break

def fight(player,forest):
    while True:
        try:
            if len(player.warriors) == 0:
                print(f'没有战士，游戏失败！')
                sys.exit(0)
            print(
                f'目前有拥有的战士名称,类型,现有生命值，最大生命值：{[(key, value.typeName, value.strength, value.maxStrength) for key, value in player.warriors.items()]}')
            name = input('请输入要攻击的战士名称：')
            if name not in player.warriors:
                print(f'没有找到名字为{name}的战士，请重新输入')
                time.sleep(1)
                continue
            player.warriors[name].fightWithMonster(forest.monster)
            print(f'{name}对{forest.monster.typeName}发起攻击，还剩{player.warriors[name].strength}生命值')
            if player.warriors[name].strength <= 0:
                print(f'{name}被{forest.monster.typeName}杀死了！')
                del player.warriors[name]
                print(f'目前还有{len(player.warriors)}个战士，还剩{player.stoneNumber}灵石')
                time.sleep(1)
                continue
            judge = input(f'剩余灵石{player.stoneNumber}，{name}是否使用灵石疗伤？(y/n)')
            if judge == 'y':
                num_healing = input(f'请输入要使用的灵石数量：')
                player.warriors[name].healing(int(num_healing))
                print(f'{name}使用{num_healing}灵石疗伤，还剩{player.warriors[name].strength}生命值')
                return True
            else:
                print('不疗伤，继续战斗')
                return True
        except Exception as e:
            print(e)
        break

# 鹰妖
class Eagle():
    typeName = '鹰妖'

# 狼妖
class Wolf():
    typeName = '狼妖'

# 森林
class Forest():
    def __init__(self,monster):
        # 该森林里面的妖怪
        self.monster = monster
def main():
    print('''
    ***************************************
    ****           游戏开始             ****
    ***************************************
    
    '''
    )

    # 森林数量
    forest_num = 7

    # 森林 列表
    forestList = []

    # 为每座森林随机产生 鹰妖或者 狼妖
    notification = '前方森林里的妖怪是：'  # 显示在屏幕上的内容
    for i in range(forest_num):
        typeName = randint(0,1)
        if typeName == 0:
            forestList.append( Forest(Eagle()) )
        else:
            forestList.append( Forest(Wolf()) )

        notification += \
            f'第{i+1}座森林里面是 {forestList[i].monster.typeName}  '

    # 显示 妖怪信息
    print(notification,end='',flush=True)
    time.sleep(1)
    print('\n'*20)
    player = Player(1000)
    hire_warriors(player)

    for i, forest in enumerate(forestList):
        print(f'你到达了第{i + 1}座森林！')
        fight(player,forest)

    print('游戏成功！')

if __name__ == '__main__':
    main()

