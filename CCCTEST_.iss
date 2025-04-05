[Setup]
AppName=CCCTEST_
AppVersion=1.0
DefaultDirName={pf}\CCCTEST_
OutputDir=C:\Users\Melvin\Desktop\Tipo Test CCC
OutputBaseFilename=InstaladorCCCTEST_
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "json\*"; DestDir: "{app}\json"; Flags: recursesubdirs
Source: "\resultados_test.json*"; DestDir: "{app}\json"; Flags: recursesubdirs

[Icons]
Name: "{group}\CCCTEST_"; Filename: "{app}\CCCTEST_.exe"
Name: "{group}\Desinstalar CCCTEST"; Filename: "{uninstallexe}"

