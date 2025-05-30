import colorama

def mod_skin(ID, ID_1):
    if ID_1 == ID[0:3] + "00":
        Show = input("\n \033[1;36mShow name? (y/n): ")
    else:
        Show = "n"
    IDB = hex(int(ID))[2:6]
    IDB = bytes.fromhex(IDB[2:4] + IDB[0:2])
    IDC = hex(int(ID_1))[2:6]
    IDC = bytes.fromhex(IDC[2:4] + IDC[0:2])
    Files = ["Actor/heroSkin.bytes", "Shop/HeroSkinShop.bytes"]
    print("\033[1;36m\n" + "-" * 60)
    for File in Files:
        All = []
        All_S = []
        Skin = ""
        S = []
        with open(File, "rb") as file:
            Code = file.read(140)
            while True:
                Num = file.read(2)
                if Num == b"":
                    break
                Number = Num[0] + Num[1] * 256 + 2
                ND = file.read(Number)
                IDH = ND[6:8]
                IDH = IDH[0] + IDH[1] * 256
                Code += Num + ND
                S.append(Num + ND)
                if IDH == int(ID[0:3]):
                    if ND[2:4] == IDB:
                        Skin = Num + ND
                    All.append(Num + ND)
        if Skin == "":
            print("\n \033[1;31m The id couldn't be found in " + File + " file!")
            IDNew = input("\n\033[1;36m  Enter an alternate skin ID: ")
            IDK = hex(int(IDNew))[2:6]
            IDK = bytes.fromhex(IDK[2:4] + IDK[0:2])
            for i in S:
                if i.find(IDK) != -1:
                    Skin = i
                    break
        for id in All:
            if IDC in id:
                All_S.append(id)
        for Id in All_S:
            Cache = Skin.replace(Skin[4:6], Id[4:6], 1)
            Cache = Cache.replace(Cache[35:44], Id[35:44], 1)
            if Show == "y":
                if Id == Skin:
                    Cache = Cache.replace(Skin[35:44], b"\x00" * 5 + b"\x14" + b"\x00" * 3, 1)
                if Id == All[0]:
                    Cache = Cache.replace(Id[35:44], Skin[35:44], 1)
            if File == Files[0]:
                if Id == All[0]:
                    ID30 = b"\x07\x00\x00\x0030" + bytes(ID[0:3] + "0", "utf8") + b"\x00"
                    XYZ = Cache[64]
                    ID0 = Cache[64: 68 + XYZ]
                    Cache = Cache.replace(ID0, ID30, 1)
                    VT = Id.find(b"Hero_")
                    NumHero = Id[VT - 4]
                    Hero = Id[VT - 4: VT + NumHero]
                    Cache = Cache.replace(b"jpg\x00\x01\x00\x00\x00\x00", b"jpg\x00" + Hero)
                    Full = Cache.count(Hero)
                    if Full > 1:
                        Cache = Cache.replace(b"jpg\x00" + Hero, b"jpg\x00\x01\x00\x00\x00\x00", Full - 1)
                    EndTheCode = hex(len(Cache) - 4)
                    if len(EndTheCode) == 5:
                        EndTheCode = EndTheCode[3:5] + "0" + EndTheCode[2:3]
                    else:
                        EndTheCode = EndTheCode[4:6] + EndTheCode[2:4]
                    EndTheCode = bytes.fromhex(EndTheCode)
                    Cache = Cache.replace(Cache[0:2], EndTheCode)
            Code = Code.replace(Id, Cache)
        with open(File, "wb") as file:
            file.write(Code)
        print("\033[1;33m\n  " + "The " + File + " file is done!")
    print("\033[1;36m\n" + "-" * 60 + "\n")


# Nhập nhiều id skin trên 1 dòng, cách nhau dấu cách
ID_Skin = input("\033[1;32mEnter Skin: ").strip().split()

# Nhập nhiều id mod trên 1 dòng, cách nhau dấu cách
ID_Mod = input("\033[1;32mEnter Id: ").strip().split()

if len(ID_Skin) != len(ID_Mod):
    print("Number of skin ids and replace ids must be the same!")
else:
    for ID, ID_1 in zip(ID_Skin, ID_Mod):
        mod_skin(ID, ID_1)
