from userInterface import MainWindow
import asyncio


async def Main():
    window = MainWindow()
    window.mainloop()



if __name__ == "__main__":
    asyncio.run(Main())