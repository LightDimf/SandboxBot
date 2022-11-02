import aiosqlite
import logging

logging.basicConfig(level=logging.INFO)

class SQL:
    @staticmethod
    async def request(db, Query: str):
        async with db.cursor() as cur:
            await cur.execute(Query)

    @staticmethod
    async def request_one(db, Query: str):
        async with db.cursor() as cur:
            res = await cur.execute(Query)
            result = await res.fetchone()
            if len(result) == 1:
                return result[0]
            else:
                return result

    @staticmethod
    async def request_all(db, Query: str):
        async with db.cursor() as cur:
            res = await cur.execute(Query)
            result = await res.fetchall()
            return result


class Account:
    maps = {
        1: "sandboxgame://?&lexp=559a9367-fe14-48c6-95eb-1779911309e1&env=prod",
        2: "map 2", #There shoud be links to the maps...
        3: "map 3",
        4: "map 4",
        5: "map 5",
        6: "map 6",
        7: "map 7",
        8: "map 8",
        9: "map 9",
        10: "map 10"
    }

    def __init__(self, log, password, wallet, proxy, status="free", currentMap=1):
        self.log = log
        self.password = password
        self.wallet = wallet
        self.proxy = proxy
        self.status = status
        self.currentMap = currentMap

    @classmethod
    async def createNew(cls, log, password, wallet, proxy):
        return cls(log, password, wallet, proxy)

    @classmethod
    async def create(cls, log):
        async with aiosqlite.connect('DataBase/Database.db') as db:
            acc = await SQL.request_one(db, f"SELECT * FROM Accounts WHERE log='{log}'")
            return cls(*acc)

    async def save(self):
        async with aiosqlite.connect('DataBase/Database.db') as db:
            existance = await SQL.request_one(db, f"SELECT EXISTS (SELECT * FROM Accounts WHERE log = '{self.log}')")
            if(existance == 0):
                await SQL.request(db, f"INSERT INTO Accounts VALUES('{self.log}', '{self.password}', '{self.wallet}', '{self.proxy}', '{self.status}', '{self.currentMap}');")
                logging.info(f"DB: {self.log} inserted")
            else:
                await SQL.request(db, f"UPDATE Accounts SET status='{self.status}', currentMap='{self.currentMap}' WHERE log='{self.log}'")
                logging.info(f"DB: {self.log} updated")

            await db.commit()

    async def take_map(self):
        return self.maps[self.currentMap]


async def startup(dispatcher):
    """Func that's called at every bot startup"""
    async with aiosqlite.connect('DataBase/Database.db') as db:
        await SQL.request(db, "CREATE TABLE IF NOT EXISTS Accounts("
                              "log varchar(40),"
                              "password varchar(40),"
                              "wallet varchar(40),"
                              "proxy varchar(42),"
                              "status varchar(5),"
                              "currentMap int)")
        await SQL.request(db, "CREATE TABLE IF NOT EXISTS Users(id int, account varchar(40))")

async def add(message_text):
    """For admin to add new account to DB"""
    account = await Account.createNew(*message_text[5:].split(":"))
    await account.save()

async def delete(message_text):
    pass


async def TEST(user_id):
#    acc = await current_acc(user_id)
    pass


async def take():
    """Take the first free account that it's see"""
    async with aiosqlite.connect('DataBase/Database.db') as db:
        account = await Account.create(await SQL.request_one(db, "SELECT log FROM Accounts WHERE status = 'free' LIMIT 1"))
        log, pas = account.log, account.password
        account.status = "taken"
        await account.save()
        return log, pas

async def show():
    async with aiosqlite.connect('DataBase/Database.db') as db:
        print(f"Accounts: {await SQL.request_all(db, 'SELECT * FROM Accounts')}")
        print(f"Users: {await SQL.request_all(db, 'SELECT * FROM Users')}")

async def bound(login, user):
    """Bounds game account to bot user"""
    async with aiosqlite.connect('DataBase/Database.db') as db:
        existance = await SQL.request_one(db, f"SELECT EXISTS (SELECT * FROM Users WHERE id = '{user}')")
        if (existance == 0):
            await SQL.request(db, f"INSERT INTO Users(id, account) VALUES('{user}', '{login}');")
            logging.info(f"DB: user {str(user)} added with {login} account")
        else:
            await SQL.request(db, f"UPDATE Users SET account='{login}' WHERE id='{user}'")
            logging.info(f"DB: user {str(user)} updated with new {login} account")

        await db.commit()


async def currentMap(user_id):
    async with aiosqlite.connect('DataBase/Database.db') as db:
        acc = await Account.create(await current_acc(user_id))
        return await acc.take_map()

async def is_first_acc(user_id):
    async with aiosqlite.connect('DataBase/Database.db') as db:
        accounts = await SQL.request_all(db, f"SELECT account FROM Users WHERE id = '{user_id}' LIMIT 2")
        if len(accounts) > 1:
            return False
        else:
            return True

async def current_acc(user_id):
    async with aiosqlite.connect('DataBase/Database.db') as db:
        accounts = await SQL.request_all(db, f"SELECT account FROM Users WHERE id = '{user_id}'")
        return accounts[-1][0]

async def map_finished(user_id):
    acc = await Account.create(await current_acc(user_id))
    logging.info(f"DB: user: {user_id}; acc: {acc.log}; map {acc.currentMap} finished")
    if acc.currentMap + 1 <= len(acc.maps):
        acc.currentMap += 1
        await acc.save()
        return 1
    else:
        return 0