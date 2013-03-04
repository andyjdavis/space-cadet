from cx_Freeze import setup,Executable

includefiles = ['resources/ground.png',
'resources/mushroom.ogg',
'resources/music.mp3',
'resources/shroom.png',
'resources/zap.ogg',
'resources/character/jump.png',
'resources/character/walk/walk0001.png',
'resources/character/walk/walk0002.png',
'resources/character/walk/walk0003.png',
'resources/character/walk/walk0004.png',
'resources/character/walk/walk0005.png',
'resources/character/walk/walk0006.png',
'resources/character/walk/walk0007.png',
'resources/character/walk/walk0008.png',
'resources/character/walk/walk0009.png',
'resources/character/walk/walk00010.png',
'resources/character/walk/walk00011.png',
'resources/enemies/fly_fly.png',
'resources/enemies/fly_normal.png',
'resources/enemies/slime_normal.png',
'resources/enemies/slime_walk.png',
'resources/maps/1.png',
'resources/maps/2.png',
'resources/maps/3.png',
'resources/maps/4.png',
'resources/maps/5.png',
'resources/maps/6.png',
'resources/maps/7.png',
'resources/maps/8.png',
'resources/maps/9.png',
'resources/maps/10.png',
'resources/maps/base.png',
]

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], 'include_files':includefiles}

setup(
    name = 'Space Cadet',
    version = '1.0',
    description = 'A simple platformer about space travellers and fungus',
    author = 'Andrew Davis',
    options = {"build_exe": build_exe_options}, 
	executables = [Executable(script="main.py", base="Win32GUI", targetName="SpaceCadet.exe")]
)
