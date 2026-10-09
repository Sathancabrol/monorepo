; Carré d'As — installeur Windows (Inno Setup 6)
;   iscc installer\setup.iss
; Produit : Installer\CarreDAs-0.1.0-Setup.exe
;
; L'installeur n'empaquette pas Python : il l'installe côté utilisateur, ce qui
; garde un installeur de quelques mégaoctets et permet les mises à jour par Git.

#define MyAppName "Carre d'As"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Carré d'As"
#define MyAppExe "CarreDAs.exe"

[Setup]
AppId={{9F2C1A5E-6D3B-4E7A-8C21-0B5D4E7F1A93}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\CarreDAs
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=..\Installer
OutputBaseFilename=CarreDAs-{#MyAppVersion}-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayName={#MyAppName} {#MyAppVersion}
WizardSmallImageFile=
; Les données utilisateur restent dans %LOCALAPPDATA%\CarreDAs :
; désinstaller ne supprime jamais le travail de la personne.

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer une icône sur le bureau"; GroupDescription: "Raccourcis:"; Flags: unchecked

[Files]
Source: "..\dist\CarreDAs\{#MyAppExe}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\CarreDAs\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\LISIBLE-MOI.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"
Name: "{group}\Dossier des données"; Filename: "{localappdata}\CarreDAs"
Name: "{group}\Désinstaller {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "Démarrer {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Messages]
french.WelcomeLabel1=Bienvenue dans l'installation de [name]
french.FinishedHeadingLabel=Installation terminée
