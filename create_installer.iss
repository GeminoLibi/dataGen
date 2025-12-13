; Inno Setup Script for Case Generator Installer
; Requires Inno Setup: https://jrsoftware.org/isinfo.php

[Setup]
AppName=Case Data Generator
AppVersion=1.0.0
AppPublisher=GeminoLibi
AppPublisherURL=https://github.com/GeminoLibi/dataGen
DefaultDirName={autopf}\CaseDataGenerator
DefaultGroupName=Case Data Generator
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=CaseDataGenerator-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\CaseGenerator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Case Data Generator"; Filename: "{app}\CaseGenerator.exe"
Name: "{group}\{cm:UninstallProgram,Case Data Generator}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Case Data Generator"; Filename: "{app}\CaseGenerator.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Case Data Generator"; Filename: "{app}\CaseGenerator.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\CaseGenerator.exe"; Description: "{cm:LaunchProgram,Case Data Generator}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  WizardForm.LicenseAcceptedRadio.Checked := True;
end;

