import bpy, os, bmesh, pathlib, re, numpy, codecs
# bpy = Blender Python   /   os = Operating System   /   bmesh = BlenderMesh (For Editing Meshes)
# pathlib = find Home Dir of BlendFile   /  re = Extract Numbers of TextFile  /  numpy = Convert Numbers

# Import Script: .mod / .xmod to Blender (Angel Game Engine) !!! Only tested with: "Red Dead Revolver Prototype 15th Jan 2002" !!!
# Made by vollkorn2             Version 1.0 
# Supported:                    Vertices / Tex1s (UVs) / Material Slots (Textures)
# Read Only (but not used):     Vertex Normlas / Vertex Colors / Tex2s / Tangents 
# Ignored Completely:           Materials (BSDF Set Up) / Primitives / Matrices / Reskins 

print("*** Start ********************************************************************************")

# Copy / Paste your Filepath for .mod / .xmod / .png Files   (!!! All Slashes must be in this direction > / < !!! Also must be a Slash at the End !!!)
PngPath =  "D:/This/Could/Be/Your/FilePath/PNGs/" 
ModPath = "D:/This/Could/Be/Your/FilePath/.mod/" 
XModPath = "D:/This/Could/Be/Your/FilePath/.xmod/" 

# Choose if you want to Break all str/stp into Tris! (True is Recommended / Fix all Bugs) (if False: Fucked Up Original faces)
Tris = True
# Choose if you want to Add the Version to the MeshName!   ( False   or   True )
AddVersion = True
# Choose if you want to Import   .mod   or   .xmod   Models!   ( False   or   True )
ModImport = True
# Choose if you want to Import complete Levels or single Models of your choice!  ( False   or   True )
SingleImport = False
# Type in the Model Name including .mod / .xmod   (Ignored if you don't use SingleImport)
SingleFile = "lvl_ai_liverystable.mod"

# *** Copy / Paste the Level Name of your Choice (including both " " Marks)
LevelName = "Other"
# *** Level List: *** (Choose "Other" for all non Level Meshes / Also needed for .xmod)
# "ai"      "anim"      "arena"     "arena2"    "arena3"    "bank"          "barber"    "bath"      "beasley"   "bossMans"
# "bridge"  "chs"       "climb"     "cloShop"   "core_"     "coreMulti"     "cover"     "cover2"    "cover3"    "cpvFlicker"
# "dm1"     "dm2"       "estate"    "flash"     "floor"     "fort"          "genStore"  "ghost"     "gunShop"   "hng"
# "jody"    "lawyer"    "mans"      "mine_"     "mineLight" "mineNite"      "msj"       "msn"       "mst"       "occlude"
# "perf75"  "resid"     "saloon"    "sher70"    "sherLo_"   "sherLo2"       "sherNite"  "sneak"     "station"   "tng"
# "tomb"    "tombInt"   "tombSal"   "tombSher"  "train"     "tunnel"        "wagonTest" "wheel"            "Other"

#***************************************************************************************************************************
#***************************************************************************************************************************
#***************************************************************************************************************************
if ModImport == True: 
    FilePath = ModPath
if ModImport == False: 
    FilePath = XModPath

RightFile = False       # Blocking "for loop" as soon as current Mesh is completed and next loop begins
RightLevel = False      # Breaks current loop if Filename has wrong Level
for Root, Dirs, file in os.walk(FilePath): 
    FileList = file
for File in FileList: 
    if RightFile == False: 
        # Check File 
        if SingleImport == True:            # Check if correct File 
            if File == SingleFile: 
                RightFile = True 
                RightLevel = True 
        else:                               # Check if Correct Level
            Length1 = len(LevelName)
            Length2 = Length1+4             # lvl_
            TempLevel = File[:Length2]
            TempLevel = TempLevel[4:]
            if LevelName == TempLevel: 
                RightLevel = True
            else: 
                RightLevel = False
            if LevelName == "Other": 
                TempLevel = File[:4]
                if not TempLevel == "lvl_":
                    RightLevel = True 
                else: 
                    RightLevel = False          # Block current loop and jump to next File
                    
        # Checking Version (Text = 1.09, 1.10 / Binary = 2.00, 2.10, 2.12)
        if RightLevel == True: 
            if File[-4:] == ".mod": 
                NewName = File[:-4]         # Delete .mod
            if File[-5:] == ".xmod": 
                NewName = File[:-5]         # Delete .xmod
      
            with open(FilePath+File, "rb") as FileToRead: 
                TempText = FileToRead.readlines()   # .read instead of .readlines ???
                Text = TempText[0]
                for Line in TempText:               # in Temptext all Lines are seperated, so I reconnect them to one Line 
                    if not Line == Text: 
                        Text += Line
                Version = Text[9:] 
                Version = float(Version[:4])
            
#***************************************************************************************************************************
#***************************************************************************************************************************
            # Text File ****************************************************************************************************
            if Version == 1.09 or Version == 1.10: 
                with open(FilePath+File, "r") as FileToRead: 
                    Text = FileToRead.readlines()
                    print("Text File:   ", Version, " ", File)
                    if Version == 1.09:             # Set FileHead
                        FileHead = 11
                    if Version == 1.10:
                        FileHead = 12
                
                    # Reading FileHead
                    Verts = Text[1]
                    Verts = int(Verts[7:])
                    Normals = Text[2]
                    Normals = int(Normals[9:])
                    Colors = Text[3]
                    Colors = int(Colors[8:])
                    Tex1s = Text[4] 
                    Tex1s = int(Tex1s[7:])
                    Tex2s = Text[5] 
                    Tex2s = int(Tex2s[7:])
                    Tangents = Text[6]
                    Tangents = int(Tangents[10:])
                    Materials = Text[7]
                    Materials = int(Materials[11:])
                    Adjuncts = Text[8]
                    Adjuncts = int(Adjuncts[10:])
                    Primitives = Text[9]
                    Primitives = int(Primitives[12:])
                    Matrices = Text[10]
                    Matrices = int(Matrices[10:])
                    if Version == 1.10:
                        Reskins = Text[11]
                        Reskins = int(Reskins[9:])
#                    print(Version, Verts, Normals, Colors, Tex1s, Tex2s, Tangents, Materials, Adjuncts, Primitives, Matrices)
#                    print(Reskins) 
                
                    VertList = []     #************************************************************************************************** 
                    StartLine = FileHead+1
                    for Line in range(Verts):
                        CurrentLine = StartLine+Line 
                        TempLine = Text[CurrentLine]
                        TempLine = TempLine[2:]                 # Delete first 2 
                        TempLine = re.split(r'(\s)', TempLine)
                        Temp = []
                        for Item in TempLine:                   # Remove Tab, Enter, Empty
                            if Item == '\t':
                                TempLine.remove(Item)
                            if Item == '\n':
                                TempLine.remove(Item)        
                        TempLine = [x for x in TempLine if x != '']
                        for Item in TempLine:                   # Add Vertex to List
                            Item = float(Item)
                            Temp.append(Item)
                        VertList.append(Temp)
#                    print(VertList)
                
                    NormList = []     #**************************************************************************************************
                    StartLine = StartLine+Verts+1
                    for Line in range(Normals):
                        CurrentLine = StartLine+Line
                        TempLine = Text[CurrentLine]
                        TempLine = TempLine[2:]                 # Delete first 2 
                        TempLine = re.split(r'(\s)', TempLine)
                        Temp = []
                        for Item in TempLine:                   # Remove Tab, Enter, Empty
                            if Item == '\t':
                                TempLine.remove(Item)
                            if Item == '\n':
                                TempLine.remove(Item)        
                        TempLine = [x for x in TempLine if x != '']
                        for Item in TempLine:                   # Add Vertex Normal to List
                            Item = float(Item)
                            Temp.append(Item)
                        NormList.append(Temp)
#                print(NormList)
                
                    ColorList = []     #**************************************************************************************************
                    StartLine = StartLine+Normals+1
                    for Line in range(Colors):
                        CurrentLine = StartLine+Line
                        TempLine = Text[CurrentLine]
                        TempLine = TempLine[2:]                 # Delete first 2 
                        TempLine = re.split(r'(\s)', TempLine)
                        Temp = []
                        for Item in TempLine:                   # Remove Tab, Enter, Empty
                            if Item == '\t':
                                TempLine.remove(Item)
                            if Item == '\n':
                                TempLine.remove(Item)        
                        TempLine = [x for x in TempLine if x != '']
                        for Item in TempLine:                   # Add Vertex Color to List
                            Item = float(Item)
                            Temp.append(Item)
                        ColorList.append(Temp)
#                    print(ColorList)    
                
                    Tex1List = []     #**************************************************************************************************
                    StartLine = StartLine+Colors+1
                    HasSpace = False                            # Some Files have one extra Space between Colors and Tex1s !!! 
                    for Line in range(Tex1s):
                        CurrentLine = StartLine+Line
                        TempLine = Text[CurrentLine]
                        if TempLine == '\n':                    # If Line is Empty
                            HasSpace = True
                            StartLine += 1                      # add extra space line for rest of Variables below / Reset for each new File
                            TempLine = Text[CurrentLine+1]      # Correcting Line for current Loop
                        TempLine = TempLine[3:]                 # Delete first 3 
                        TempLine = re.split(r'(\s)', TempLine)
                        Temp = []
                        for Item in TempLine:                   # Remove Tab, Enter, Empty
                            if Item == '\t':
                                TempLine.remove(Item)
                            if Item == '\n':
                                TempLine.remove(Item)        
                        TempLine = [x for x in TempLine if x != '']
                        for Item in TempLine:                   # Add Tex1 to List
                            Item = float(Item)
                            Temp.append(Item)
                        Tex1List.append(Temp)
#                    print(Tex1List)  
                
                    Tex2List = []     #**************************************************************************************************
                    StartLine = StartLine+Tex1s+1
                    if not Tex2s == 0:
                        for Line in range(Tex2s):
                            CurrentLine = StartLine+Line
                            TempLine = Text[CurrentLine]
                            TempLine = TempLine[2:]                 # Delete first 2 
                            TempLine = re.split(r'(\s)', TempLine)
                            Temp = []
                            for Item in TempLine:                   # Remove Tab, Enter, Empty
                                if Item == '\t':
                                    TempLine.remove(Item)
                                if Item == '\n':
                                    TempLine.remove(Item)        
                            TempLine = [x for x in TempLine if x != '']
                            for Item in TempLine:                   # Add Tex2 to List
                                Item = float(Item)
                                Temp.append(Item)
                            Tex2List.append(Temp)
#                        print(Tex2List) 
                    else: 
                        StartLine = StartLine-1                     # Remove 1 Empty Line if there are no Tex2s
                
                    MaterialList = []     #**************************************************************************************************
                    PacketList = []
                    TextureList = []
                    StartLine = StartLine+Tex2s+2       # There are 2 Empty Lines between Tex2s and Material Slots
                    # StartLine changes incremental !!! 
                    for Line in range(Materials):
                        MatName = Text[StartLine]
                        MatName = MatName[4:]
                        MatName = MatName[:-2]
                        MaterialList.append(MatName)
                        StartLine += 1
                        PacketNr = Text[StartLine]
                        PacketNr = int(PacketNr[10:])
                        PacketList.append(PacketNr)
                        StartLine += 2
                        TexNr = Text[StartLine]
                        TexNr = int(TexNr[11:]) 
                        StartLine += 5
                        if not TexNr == 0:              
                            Texture = Text[StartLine]
                            Texture = Texture[12:]
                            Texture = Texture[:-1]
                            StartLine += 1              # Add Texture Slot
                        else: 
                            Texture = "Empty"
                        TextureList.append(Texture)
                        if not Version == 1.09:
                            StartLine += 1              # Add attributes Slot
                        StartLine += 2                  # Jump to next Material Slot
#                    print(MaterialList, PacketList, TextureList) 
                    
                    IndexVerts = []         #**************************************************************************************************
                    IndexNormals = []
                    IndexColors = []
                    IndexTex1s = []
                    IndexTex2s = []
                    IndexTangents = []
                    MatSlots = []
                    Faces = []
                    MatCounter = 0
                    # StartLine already correct from MaterialSlot Loop
                    # StartLine changes incremental !!! 
                    for MatSlot in MaterialList:
                        PacketNr = PacketList[MatCounter]
                        for Packet in range(PacketNr): 
                            PacketHead = []
                            TempLine = Text[StartLine]
                            if TempLine == "\n":            # Some files has one Extra space between some Packets
                                StartLine += 1
                                TempLine = Text[StartLine]
                            TempLine = TempLine[7:]
                            TempLine = TempLine[:-2]
                            TempLine = re.split(r'(\s)', TempLine)
                            TempLine = [x for x in TempLine if x != '']
                            TempLine = [x for x in TempLine if x != ' ']
                            for Int in TempLine: 
                                PacketHead.append(int(Int))
                            StartLine += 1
                            TempVerts = []
                            TempNormals = []
                            TempColors = []
                            TempTex1s = []
                            TempTex2s = []
                            TempTangents = []
                            for adj in range(PacketHead[0]):                    # Save Adjuncts
                                TempStartLine = StartLine+adj
                                TempLine = Text[TempStartLine]
                                TempLine = TempLine[6:]
                                TempLine = re.split(r'(\s)', TempLine)
                                TempLine = [x for x in TempLine if x != '']
                                TempLine = [x for x in TempLine if x != ' ']
                                TempLine = [x for x in TempLine if x != '\n']
                                TempVerts.append(int(TempLine[0])) 
                                TempNormals.append(int(TempLine[1]))
                                TempColors.append(int(TempLine[2]))
                                TempTex1s.append(int(TempLine[3]))
                                TempTex2s.append(int(TempLine[4]))
                                TempTangents.append(int(TempLine[5]))
                            StartLine += PacketHead[0]                          # Jump to str/stp or reskins
                            try: 
                                StartLine += PacketHead[3]                      # Try to Skip Reskins if exists
                            except: 
                                StartLine = StartLine 
                            
                            for str in range(PacketHead[1]):                    # Save str/stp
                                TempStartLine = StartLine+str
                                Length = Text[TempStartLine]                    # Length = Number of Indices per Line (as CountNumber)
                                Length = Length[8:]
                                Length = Length[:2]
                                Length = re.split(r'(\s)', Length)
                                Length = [x for x in Length if x != '']
                                Length = [x for x in Length if x != ' ']
                                Length = Length[0]
                                Length = int(Length)                              
                                TempLine = Text[TempStartLine]
                                TempLine = TempLine[12:]
                                TempLine = re.split(r'(\s)', TempLine)
                                TempLine = [x for x in TempLine if x != '']
                                TempLine = [x for x in TempLine if x != ' ']
                                TempLine = [x for x in TempLine if x != '\n']
                                
                                TempList = []
                                IndexNr = 0
                                Foreward = True
                                Length2 = Length-1                              # Length2 = Number of Indices per Line (as Index)
                                Length3 = Length-2                              # Length3 = Number of Tris
                                if Tris == True: 
                                    for Index in range(Length3):                # Reorder Indices of str/stp to Tris
                                        Temp = []
                                        Nr1 = TempLine[Index]
                                        Nr1 = int(Nr1)
                                        Temp.append(Nr1)
                                        Nr2 = TempLine[Index+1]
                                        Nr2 = int(Nr2)
                                        Temp.append(Nr2)
                                        Nr3 = TempLine[Index+2]
                                        Nr3 = int(Nr3)
                                        Temp.append(Nr3)
                                        TempList.append(Temp)
                                if Tris == False: 
                                    for Index in range(Length):                     # Reorder Indices of str/stp to correct Result of Faces
                                        Run = True
                                        if Foreward == True:
                                            if IndexNr < Length2 and Run == True: 
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr += 2
                                                Run = False
                                            if IndexNr == Length2 and Run == True:
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr -= 1
                                                Foreward = False
                                                Run = False
                                            if IndexNr > Length2 and Run == True:        # Go to Last Index, append and jump 2 Indices back 
                                                IndexNr -= 1
                                                Foreward = False
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr -= 2
                                                Run = False
                                        if Foreward == False and Run == True:
                                            if IndexNr > 0: 
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr -= 2
                                
                                if Tris == False:                           # Converts Variable to List by adding an Integer 
                                    Temp = TempList
                                    TempList = []
                                    TempList.append(Temp)
                                    TempList.append(-1)
                                for List in TempList:                       # Stop Second Loop if Tris == False
                                    if List == -1: 
                                        break
                                    TempListVerts = [] 
                                    TempListNormals = [] 
                                    TempListColors = [] 
                                    TempListTex1s = []
                                    TempListTex2s = [] 
                                    TempListTangents = []
                                    for Index in List:                      # Save Vertex Indices to Faces
                                        TempV = TempVerts[Index]
                                        TempListVerts.append(TempV)
                                        TempN = TempNormals[Index]
                                        TempListNormals.append(TempN)
                                        TempC = TempColors[Index]
                                        TempListColors.append(TempC)
                                        TempT1 = TempTex1s[Index]
                                        TempListTex1s.append(TempT1)
                                        TempT2 = TempTex2s[Index]
                                        TempListTex2s.append(TempT2)
                                        TempT = TempTangents[Index]
                                        TempListTangents.append(TempT)
                                    Faces.append(TempListVerts)
                                    IndexNormals.append(TempListNormals)
                                    IndexColors.append(TempListColors)
                                    IndexTex1s.append(TempListTex1s) 
                                    IndexTex2s.append(TempListTex2s)
                                    IndexTangents.append(TempListTangents)
                                    MatSlots.append(MatCounter)             # Save Material Slot to Face Index                
                                
                            StartLine += PacketHead[1]          # Jump to end of str/stp 
                            StartLine += 3                      # Jump to next Packet begin
                        MatCounter += 1                         # Mat Counter, next Material Slot
#                    print(IndexVerts, IndexNormals, IndexColors, IndexTex1s, IndexTex2s, IndexTangents, Faces, MatSlots)

#***************************************************************************************************************************
#***************************************************************************************************************************
            # Binary File ******************************************************************************************************
            else:
                with open(FilePath+File, "rb") as FileToRead: 
                    TempText = FileToRead.readlines()           # .read instead of .readlines ??? 
                    Text = TempText[0]
                    print("Binary File: ", Version, " ", File)
                    for Line in TempText:                       # in Temptext all Lines are seperated, so I reconnect them to one Line 
                        if not Line == Text: 
                            Text += Line
                    Version = Text[9:] 
                    Version = float(Version[:4])
                    Text = Text[14:]                            # Text without Version and first Byte
                    TextHead = Text[:44] 
                    # Reading FileHead
                    ListHead = numpy.frombuffer(TextHead, dtype=numpy.int16)    # Byte to int16
                    Verts = ListHead[0]
                    Normals = ListHead[2]
                    Colors = ListHead[4]
                    Tex1s = ListHead[6] 
                    Tex2s = ListHead[8] 
                    Tangents = ListHead[10]
                    Materials = ListHead[12]
                    Adjuncts = ListHead[14]
                    Primitives = ListHead[16]
                    Matrices = ListHead[18]
                    FileHead = 40                               # only for version 2.0 (No Reskins)
                    Reskins = 0
                    if not Version == 2.0:
                        Reskins = ListHead[20]
                        FileHead = 44
#                    print(Version, Verts, Normals, Colors, Tex1s, Tex2s, Tangents, Materials, Adjuncts, Primitives, Matrices)
#                    print(Reskins)
                    
                    VertList = []     #**************************************************************************************************
                    Text = Text[FileHead:]              # Remove FileHead from Text
                    VertByteNr = Verts*3*4              # Number of Vertices * 3 Floats(Vector) * 4 Bytes   /   Get Total Number of Bytes used for Vertices
                    TextVerts = Text[:VertByteNr]       # Remove all except Verts
                    TempFloats = numpy.frombuffer(TextVerts, dtype=numpy.float32)     # Byte to float32
                    CurrentFloat = 0 
                    TempList = []
                    for Float in TempFloats: 
                        TempList.append(float(Float))
                        CurrentFloat += 1
                        if CurrentFloat == 3: 
                            VertList.append(TempList)
                            TempList = []
                            CurrentFloat = 0
#                    print(VertList)
                    
                    NormList = []     #**************************************************************************************************
                    Text = Text[VertByteNr:]            # Remove VertByteNr from Text
                    NormByteNr = Normals*3*4            # Number of Normals * 3 Floats(Vector) * 4 Bytes   /   Get Total Number of Bytes used for Normals
                    TextNorms = Text[:NormByteNr]       # Remove all except Normals
                    TempFloats = numpy.frombuffer(TextNorms, dtype=numpy.float32)     # Byte to float32
                    CurrentFloat = 0 
                    TempList = []
                    for Float in TempFloats: 
                        TempList.append(float(Float))
                        CurrentFloat += 1
                        if CurrentFloat == 3: 
                            NormList.append(TempList)
                            TempList = []
                            CurrentFloat = 0
#                    print(NormList)
                    
                    ColorList = []     #**************************************************************************************************
                    Text = Text[NormByteNr:]            # Remove NormByteNr from Text
                    ColorByteNr = Colors*4*4            # Number of Colors * 4 (RGBA) * 4 Bytes   /   Get Total Number of Bytes used for Colors
                    TextColors = Text[:ColorByteNr]     # Remove all except Colors
                    TempFloats = numpy.frombuffer(TextColors, dtype=numpy.float32)     # Byte to float32
                    CurrentFloat = 0 
                    TempList = []
                    for Float in TempFloats: 
                        TempList.append(float(Float))
                        CurrentFloat += 1
                        if CurrentFloat == 4: 
                            ColorList.append(TempList)
                            TempList = []
                            CurrentFloat = 0
#                    print(ColorList)
                    
                    Tex1List = []     #**************************************************************************************************
                    Text = Text[ColorByteNr:]           # Remove ColorByteNr from Text
                    Tex1ByteNr = Tex1s*2*4              # Number of Tex1 * 2 (UV) * 4 Bytes   /   Get Total Number of Bytes used for Tex1
                    TextTex1 = Text[:Tex1ByteNr]        # Remove all except Tex1
                    TempFloats = numpy.frombuffer(TextTex1, dtype=numpy.float32)     # Byte to float32
                    CurrentFloat = 0 
                    TempList = []
                    for Float in TempFloats: 
                        TempList.append(float(Float))
                        CurrentFloat += 1
                        if CurrentFloat == 2: 
                            Tex1List.append(TempList)
                            TempList = []
                            CurrentFloat = 0
#                    print(Tex1List)
                    
                    Tex2List = []     #**************************************************************************************************
                    Text = Text[Tex1ByteNr:]
                    Tex2ByteNr = Tex2s*2*4              # Number of Tex2 * 2 (UV) * 4 Bytes   /   Get Total Number of Bytes used for Tex2
                    TextTex2 = Text[:Tex2ByteNr]        # Remove all except Tex2
                    TempFloats = numpy.frombuffer(TextTex2, dtype=numpy.float32)     # Byte to float32
                    CurrentFloat = 0 
                    TempList = []
                    for Float in TempFloats: 
                        TempList.append(float(Float))
                        CurrentFloat += 1
                        if CurrentFloat == 2: 
                            Tex2List.append(TempList)
                            TempList = []
                            CurrentFloat = 0
#                    print(Tex2List)
                    
                    MaterialList = []     #**************************************************************************************************
                    PacketList = []
                    TextureList = []
                    Text = Text[Tex2ByteNr:]                # Remove Tex2ByteNr from Text
                    for Slot in range(Materials): 
                        TempString = Text[:70]              # Yes, there are Material Names up to (at least) 63 Characters !!!
                        TempStringList = []
                        for Char in TempString:             # Byte to Int       (needed to avoid error)
                            TempStringList.append(Char) 
                        TempString = ""
                        for Char in TempStringList:         # Int to Character  (needed to avoid error)
                            Char = chr(Char)
                            TempString += Char
                        TempString = re.split(r'(\s)', TempString)
                        MatName = TempString[0]
                        MaterialList.append(MatName)    # Save Material Name
                        Length = len(MatName)
                        Text = Text[Length+1:]          # Remove Length of Material Name + Space
                        TempText = Text[:10]
                        PacketNr = numpy.frombuffer(TempText, dtype=numpy.int16)        # Byte to int16
                        PacketList.append(PacketNr[0])
                        TempText = TempText[8:]
                        TextureNr = numpy.frombuffer(TempText, dtype=numpy.int16)       # Byte to int16
                        TextureNr = TextureNr[0]
                        Text = Text[16+32+16:]          # Remove: 16 Bytes for Packets - illum / 32 Bytes for Settings / 16 Bytes for IDK
                        if TextureNr != 0:
                            TempString = Text[:70] 
                            TempStringList = []
                            for Char in TempString:             # Byte to Int       (needed to avoid error)
                                TempStringList.append(Char) 
                            TempString = ""
                            for Char in TempStringList:         # Int to Character  (needed to avoid error)
                                Char = chr(Char)
                                TempString += Char
                            TempString = re.split(r'(\s)', TempString)
                            TexName = TempString[0]
                            if TexName == "":               # in case there is 1 Texture defined but it's Name is empty (lvl_floor_bound_deerhead_comp)
                                TexName = "EmptyTexture"
                            TextureList.append(TexName)     # Save Texture Name
                            Length = len(TexName)
                            Text = Text[Length+1:] 
                        else: 
                            TextureList.append("Empty")     # Save Empty Texture Name
                            
                        TempString = Text[:4]
                        CopyText = ""
                        for Char in TempString: 
                            Char = chr(Char)
                            CopyText += Char
                        if CopyText == "copy":           # Only "lvl_bath_ceiling_2p.mod" has "TextureName copy " (as ByteString)
                            Text = Text[5:]
                            
                        if not Version == 2.0: 
                            Text = Text[4:]                 # Remove Attributes / Version 2.0 doesn't have Attributes
#                    print(MaterialList, TextureList, PacketList)
                    
                    # Read Packets   **********************************************************************************************************
                    IndexVerts = []
                    IndexNormals = []
                    IndexColors = []
                    IndexTex1s = []
                    IndexTex2s = []
                    IndexTangents = []
                    MatSlots = []
                    Faces = []
                    MatCounter = 0
                    Hat_Coc_Lod = False         # hat_coc_lod has always 3 Verts and Definition of str/stp is 0 instead of 1 or 2
                    if NewName in ["hat_coc_lod_01", "hat_coc_lod_02", "hat_coc_lod_03"]:
                        Hat_Coc_Lod = True
                    
                    for MatSlot in MaterialList:
                        if NewName == "lvl_train_jailWagon" and MatSlot == "lambert20SG":   # Breaks Loop for last Material Slot to avoid error
                            break                                                           # Several Missing Textures in this File 
                        if NewName == "shitnostrip":    # This Model has no Faces (strips) at all
                            break
                        PacketNr = PacketList[MatCounter]
                        for Packet in range(PacketNr): 
                            if Version == 2.0 or Version == 2.10: 
                                V_Head = 16                 # V_Head = Number of Bytes for PacketHead
                                V_Bytes = 4                 # V_Bytes = Number of Bytes per Integer
                                V_Adjunct = 24              # V_Adjunct = Number of Bytes for each Line of Adjunct
                                V_str = 4                   # V_str = Number of Bytes for each Line of str/stp (also used for Matrices) 
                                V_Numpy = 2                 # Multiply Index with V_Numpy to correct Index for Version 2.0
#                                print("Version 2.0 or 2.10")
                            if not Version == 2.0 and not Version == 2.10: 
                                V_Head = 8
                                V_Bytes = 2
                                V_Adjunct = 12
                                V_str = 1
                                V_Numpy = 1
#                                print("Version 2.12")
   
                            PacketHead = []
                            PacketHead = Text[:V_Head]
                            PacketHead = numpy.frombuffer(PacketHead, dtype=numpy.int16)    # Byte to int16
                            TempVerts = []
                            TempNormals = []
                            TempColors = []
                            TempTex1s = []
                            TempTex2s = []
                            TempTangents = []
                            Text = Text[V_Head:]                                # Delete Packet Head
                            ByteNr = PacketHead[0]*6*V_Bytes                    # Number of Adjuncts * 6 Indices per Line * Number of Bytes (depending on Version)
                            TempText = Text[:ByteNr]                            # Remove All except Adjuncts
                            for adj in range(PacketHead[0]):        # Save Adjuncts
                                TempLine = TempText[:V_Adjunct]                 # Remove All except current Line Adjunct
                                TempLine = numpy.frombuffer(TempLine, dtype=numpy.int16)
                                TempVerts.append(TempLine[0*V_Numpy])           # *V_Numpy is correcting Index for Version 2.0
                                TempNormals.append(TempLine[1*V_Numpy])
                                TempColors.append(TempLine[2*V_Numpy])
                                TempTex1s.append(TempLine[3*V_Numpy])
                                TempTex2s.append(TempLine[4*V_Numpy])
                                TempTangents.append(TempLine[5*V_Numpy])   
                                TempText = TempText[V_Adjunct:]                 # Delete 1 Line Adjunct (for next Loop)
                            Text = Text[ByteNr:]                                # Delete Adjuncts
                            
                            if not Version == 2.0:
                                ByteNr = PacketHead[3]*(2*2+4*4)                    # Number of Reskins * [2(Int16) * 2(Bytes) + 4(float32) * 4(Bytes)]
                                Text = Text[ByteNr:]                                # Delete (Skip) Reskins

                            for str in range(PacketHead[1*V_Numpy]):            # Save str/stp
                                if not Hat_Coc_Lod == True:                         # hat_coc_lod has always 3 Verts and Definition of str/stp is 0 instead of 1 or 2
                                    Text = Text[V_str:]                             # Remove First Byte (Definition of str or stp (Uselsess?))
                                Length = Text[:V_str]                               # Length = Number of Indices per str/stp (as CountNumber)
                                Length = numpy.frombuffer(Length, dtype=numpy.int8)
                                Length = int(Length[0])
                                if Hat_Coc_Lod == True:                             # hat_coc_lod has always 3 Verts and Definition of str/stp is 0 instead of 1 or 2
                                    Length = 3
                                Text = Text[V_str:]                                 # Remove Second Byte (Number of Indices for str/stp)
                                TempLine = []
                                for Byte in range(Length):                      # Save str/stp indices
                                    Byte = Text[:V_str]
                                    Byte = numpy.frombuffer(Byte, dtype=numpy.int8)
                                    Byte = int(Byte[0])
                                    TempLine.append(Byte)
                                    Text = Text[V_str:]                             # Remove Current Byte
                                TempList = []
                                IndexNr = 0
                                Foreward = True
                                Length2 = Length-1                                  # Length = Number of Indices per str/stp (as Index)
                                Length3 = Length-2                                  # Length3 = Number of Tris
                                if Tris == True: 
                                    for Index in range(Length3):                    # Reorder Indices of str/stp to Tris
                                        Temp = []
                                        Nr1 = TempLine[Index]
                                        Nr1 = int(Nr1)
                                        Temp.append(Nr1)
                                        Nr2 = TempLine[Index+1]
                                        Nr2 = int(Nr2)
                                        Temp.append(Nr2)
                                        Nr3 = TempLine[Index+2]
                                        Nr3 = int(Nr3)
                                        Temp.append(Nr3)
                                        TempList.append(Temp)
                                if Tris == False: 
                                    for Index in range(Length):                         # Reorder Indices of str/stp to correct Result of Faces
                                        Run = True
                                        if Foreward == True:
                                            if IndexNr < Length2 and Run == True: 
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr += 2
                                                Run = False
                                            if IndexNr == Length2 and Run == True:
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr -= 1
                                                Foreward = False
                                                Run = False
                                            if IndexNr > Length2 and Run == True:        # Go to Last Index, append and jump 2 Indices back 
                                                IndexNr -= 1
                                                Foreward = False
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr -= 2
                                                Run = False
                                        if Foreward == False and Run == True:
                                            if IndexNr > 0: 
                                                Nr = TempLine[IndexNr]
                                                Nr = int(Nr)
                                                TempList.append(Nr)
                                                IndexNr -= 2
                                
                                if Tris == False:                           # Converts Variable to List by adding an Integer 
                                    Temp = TempList
                                    TempList = []
                                    TempList.append(Temp)
                                    TempList.append(-1)
                                for List in TempList:                       # Stop Second Loop if Tris == False
                                    if List == -1: 
                                        break
                                    TempListVerts = [] 
                                    TempListNormals = [] 
                                    TempListColors = [] 
                                    TempListTex1s = [] 
                                    TempListTex2s = [] 
                                    TempListTangents = [] 
                                    for Index in List:                      # Save Vertex / Normal / Color / Tex1  Indices per Face
                                        TempV = TempVerts[Index]
                                        TempListVerts.append(TempV)
                                        TempN = TempNormals[Index]
                                        TempListNormals.append(TempN)
                                        TempC = TempColors[Index]
                                        TempListColors.append(TempC)
                                        TempT1 = TempTex1s[Index]
                                        TempListTex1s.append(TempT1)
                                        TempT2 = TempTex2s[Index]
                                        TempListTex2s.append(TempT2)
                                        TempT = TempTangents[Index]
                                        TempListTangents.append(TempT)
                                    Faces.append(TempListVerts)
                                    IndexNormals.append(TempListNormals)
                                    IndexColors.append(TempListColors)
                                    IndexTex1s.append(TempListTex1s) 
                                    IndexTex2s.append(TempListTex2s)
                                    IndexTangents.append(TempListTangents)
                                    MatSlots.append(MatCounter)
                            Text = Text[PacketHead[2*V_Numpy]*V_str:]           # Delete (Skip) Matrices
                        MatCounter += 1
#                    print(IndexVerts, IndexNormals, IndexColors, IndexTex1s, IndexTex2s, IndexTangents, Faces, MatSlots)
                            
#***************************************************************************************************************************
#***************************************************************************************************************************
            # Create Models ************************************************************************************************
            Edges = []
            if AddVersion == True: 
                if Version == 1.09:
                    NewName = "1.09_"+NewName
                elif Version == 1.10:
                    NewName = "1.10_"+NewName
                elif Version == 2.00:
                    NewName = "2.00_"+NewName
                elif Version == 2.10:
                    NewName = "2.10_"+NewName
                elif Version == 2.12:
                    NewName = "2.12_"+NewName
                else: 
                    print("New Version: ",Version)

            MeshFile = bpy.data.meshes.new(NewName)
            MeshFile.from_pydata(VertList, Edges, Faces)
            Mesh = bpy.data.objects.new(NewName, MeshFile) 
            bpy.context.collection.objects.link(Mesh)
            Mesh.rotation_euler[0] = 1.570796                   # X + 90°
            
            MatCounter = 0
#            for Material in MaterialList:                      # Overlapping Materials with Different Textures
#                if Material in bpy.data.materials: 
#                    NewMat = bpy.data.materials[Material]
            for Texture in TextureList:
                if Texture in bpy.data.images: 
                    NewMat = bpy.data.materials[Texture]
                else:
#                    bpy.data.materials.new(name=Material)      # Overlapping Materials with Different Textures
#                    NewMat = bpy.data.materials[Material]
                    bpy.data.materials.new(name=Texture)
                    NewMat = bpy.data.materials[Texture]
                    NewMat.use_nodes = True
                    if not TextureList[MatCounter] == "Empty" and not TextureList[MatCounter] == "EmptyTexture":
                        try: 
                            bpy.data.images.load(PngPath+TextureList[MatCounter]+".png",   check_existing=True)
                            Nodes = NewMat.node_tree.nodes
                            Nodes.get('Material Output')
                            Nodes.get('Material Output').location = (400, 20)
                            Nodes.get('Principled BSDF')
                            Nodes.get('Principled BSDF').location = (0, 0)
                            ImageNode = Nodes.new('ShaderNodeTexImage')             # New Image Node
                            ImageNode.image = bpy.data.images[TextureList[MatCounter]+".png"]
                            ImageNode.location = (-400, 000)
                            NewMat.node_tree.links.new(ImageNode.outputs['Color'], Nodes.get('Principled BSDF').inputs[0])      # Link
                        except: 
                            print("Missing Texture: ", TextureList[MatCounter])
                bpy.data.objects[NewName].data.materials.append(NewMat)
                MatCounter += 1
                
            bpy.context.view_layer.objects.active = Mesh
            UV = Mesh.data.uv_layers.new()
            Mesh.data.uv_layers.active = UV
            FaceCounter = 0
            for Face in Mesh.data.polygons: 
                Face.material_index = MatSlots[FaceCounter]
                UV_IndexList = IndexTex1s[FaceCounter]
                VN_IndexList = IndexNormals[FaceCounter]
                FN_Map = Face.normal                                # Not Used
                VertCounter = 0
                for Vert_Index, Loop_Index in zip(Face.vertices, Face.loop_indices):
                    UV_Index = UV_IndexList[VertCounter]
                    UV_Map = Tex1List[UV_Index] 
                    UV.data[Loop_Index].uv = (UV_Map[0], UV_Map[1])
                    VN_Index = VN_IndexList[VertCounter]            # Not Used
                    VN_Map = NormList[VN_Index]                     # Not Used
                    VertCounter += 1
                FaceCounter += 1
                