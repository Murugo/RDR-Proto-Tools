How to run: Mod2Blender.py

1. Open Blender
2. Replace Timeline Panel with Text Editor (or just go to the scripting panel)
3. Open Mod2Blender.py 
4. Copy Paste all your Filepaths into the script (.png / .mod / .xmod)
5. Set up the Variables (Tris / AddVersion / ModImport / SingleImport / SingleFile / LevelName)
6. Don't forget to Correct all Slashes for Filepaths to this direction / (Add a Slash at the End)
7. Run Script

Tris: 		True is needed for correct Faces / False is needed for Original but Fucked Faces
AddVersion: 	True = 2.00_MeshName / False = MeshName
ModImport: 	True = Import .mod Files / False = Import .xmod Files 
		(Level "Other" must be selected for .xmod)
SingleImport: 	True = Import only File named in SingleFile / False = Import Complete Level
SingleFile: 	Copy/Paste your filename for SingleImport including extension (.mod/.xmod)
LevelName: 	Copy/Paste the LevelName or "Other" for all non Level Meshes (SingleImport must be False)