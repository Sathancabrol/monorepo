# Bone Setup — wizard sombre (STA obligatoire)
# Look : setup classic (bandeau, rose, barre). Pas une copie d'une marque tierce.
Add-Type -AssemblyName PresentationFramework, PresentationCore, WindowsBase, System.Windows.Forms | Out-Null

$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $Here 'payload'
$InstallDir = Join-Path $env:LOCALAPPDATA 'Bone'
$Perms = '380172094528'
$Portal = 'https://discord.com/developers/applications'
$script:Py = $null
$script:Token = ''
$script:ClientId = ''
$script:Page = 0
$script:Busy = $false

if (-not (Test-Path $Payload)) {
    [System.Windows.MessageBox]::Show("Extraie TOUT le zip, puis relance INSTALLER.bat.", "Bone Setup") | Out-Null
    exit 1
}

$side = Join-Path $Payload 'assets\setup-sidebar.png'
if (-not (Test-Path $side)) { $side = Join-Path $Here 'sidebar.png' }
$sideUri = ([Uri](Resolve-Path $side)).AbsoluteUri

$xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Bone Setup" Width="920" Height="560" ResizeMode="NoResize"
        WindowStartupLocation="CenterScreen" Background="#0A0A0D"
        FontFamily="Segoe UI">
  <Window.Resources>
    <Style TargetType="Button" x:Key="N">
      <Setter Property="Width" Value="108"/>
      <Setter Property="Height" Value="32"/>
      <Setter Property="Margin" Value="6,0,0,0"/>
      <Setter Property="Foreground" Value="#F4E8EF"/>
      <Setter Property="Background" Value="#1A0C14"/>
      <Setter Property="BorderBrush" Value="#3A1028"/>
      <Setter Property="FontSize" Value="13"/>
    </Style>
  </Window.Resources>
  <Grid>
    <Grid.ColumnDefinitions>
      <ColumnDefinition Width="280"/>
      <ColumnDefinition Width="*"/>
    </Grid.ColumnDefinitions>
    <Grid Grid.Column="0">
      <Image Stretch="UniformToFill" Source="$sideUri"/>
      <Border VerticalAlignment="Bottom" Padding="16,18">
        <StackPanel>
          <TextBlock Text="BONE" FontSize="34" FontWeight="Bold" Foreground="White"/>
          <TextBlock Text="SETUP WIZARD  ·  V1.0" Foreground="#FF6EB0" FontSize="11" Margin="0,4,0,0"/>
        </StackPanel>
      </Border>
    </Grid>
    <Grid Grid.Column="1" Background="#121216">
      <Grid.RowDefinitions>
        <RowDefinition Height="36"/>
        <RowDefinition Height="*"/>
        <RowDefinition Height="64"/>
      </Grid.RowDefinitions>
      <Border Grid.Row="0" Background="#0E0E12" BorderBrush="#2A1220" BorderThickness="0,0,0,1" Padding="16,0">
        <TextBlock VerticalAlignment="Center" Foreground="#9A8894" FontSize="12"
                   Text="Bone Setup — South Park agent for Discord"/>
      </Border>
      <Grid Grid.Row="1" Margin="32,28,32,12" Name="Body"/>
      <Border Grid.Row="2" Background="#0E0E12" BorderBrush="#2A1220" BorderThickness="0,1,0,0">
        <StackPanel Orientation="Horizontal" HorizontalAlignment="Right" VerticalAlignment="Center" Margin="0,0,20,0">
          <Button Name="BtnBack" Content="Back" Style="{StaticResource N}"/>
          <Button Name="BtnCancel" Content="Cancel" Style="{StaticResource N}"/>
          <Button Name="BtnNext" Content="Next &gt;" Style="{StaticResource N}" FontWeight="Bold"/>
        </StackPanel>
      </Border>
    </Grid>
  </Grid>
</Window>
"@

$window = [Windows.Markup.XamlReader]::Parse($xaml)
$body = $window.FindName('Body')
$btnBack = $window.FindName('BtnBack')
$btnCancel = $window.FindName('BtnCancel')
$btnNext = $window.FindName('BtnNext')
$btnNext.Background = [Windows.Media.BrushConverter]::new().ConvertFrom('#C41864')
$btnNext.BorderBrush = [Windows.Media.BrushConverter]::new().ConvertFrom('#FF6EB0')
$btnNext.Foreground = [Windows.Media.Brushes]::White

function Clear-Body { $body.Children.Clear(); $body.RowDefinitions.Clear() }
function T([string]$text, [int]$size=22, [string]$color='#F4E8EF') {
    $tb = New-Object Windows.Controls.TextBlock
    $tb.Text = $text; $tb.FontSize = $size; $tb.Foreground = $color
    $tb.TextWrapping = 'Wrap'; $tb.Margin = '0,0,0,10'
    return $tb
}
function PinkNext([string]$label) { $btnNext.Content = $label; $btnNext.IsEnabled = $true }

function Show-Welcome {
    Clear-Body
    $body.Children.Add((T 'Welcome to Bone Setup')) | Out-Null
    $body.Children.Add((T "Cet assistant installe Bone — l'agent South Park pour Discord — puis t'ouvre le choix du serveur." 14 '#9A8894')) | Out-Null
    $body.Children.Add((T "Laisse la fenetre ouverte. Kenny s'occupe deja du reste." 14 '#9A8894')) | Out-Null
    $body.Children.Add((T 'Clique Next pour continuer.' 13 '#9A8894')) | Out-Null
    $btnBack.IsEnabled = $false
    PinkNext 'Next >'
}

function Show-Options {
    Clear-Body
    $body.Children.Add((T 'Destination & components')) | Out-Null
    $body.Children.Add((T "Dossier : $InstallDir" 13 '#FF6EB0')) | Out-Null
    $script:ChkDesk = New-Object Windows.Controls.CheckBox
    $script:ChkDesk.Content = 'Raccourci Bureau'; $script:ChkDesk.IsChecked = $true; $script:ChkDesk.Foreground = '#F4E8EF'; $script:ChkDesk.Margin = '0,8,0,4'
    $script:ChkStart = New-Object Windows.Controls.CheckBox
    $script:ChkStart.Content = 'Menu Demarrer'; $script:ChkStart.IsChecked = $true; $script:ChkStart.Foreground = '#F4E8EF'; $script:ChkStart.Margin = '0,4'
    $script:ChkBoot = New-Object Windows.Controls.CheckBox
    $script:ChkBoot.Content = 'Lancer Bone au demarrage de Windows'; $script:ChkBoot.IsChecked = $true; $script:ChkBoot.Foreground = '#F4E8EF'; $script:ChkBoot.Margin = '0,4'
    $body.Children.Add($script:ChkDesk) | Out-Null
    $body.Children.Add($script:ChkStart) | Out-Null
    $body.Children.Add($script:ChkBoot) | Out-Null
    $btnBack.IsEnabled = $true
    PinkNext 'Install'
}

function Show-Install {
    Clear-Body
    $body.Children.Add((T 'Installing')) | Out-Null
    $script:Now = T 'Preparation…' 14 '#9A8894'
    $body.Children.Add($script:Now) | Out-Null
    $script:Log = New-Object Windows.Controls.TextBox
    $script:Log.IsReadOnly = $true; $script:Log.Height = 210
    $script:Log.Background = '#070709'; $script:Log.Foreground = '#FFB6D5'
    $script:Log.FontFamily = 'Consolas'; $script:Log.FontSize = 12
    $script:Log.VerticalScrollBarVisibility = 'Auto'
    $script:Log.BorderBrush = '#2A1220'; $script:Log.Margin = '0,0,0,10'
    $body.Children.Add($script:Log) | Out-Null
    $script:Bar = New-Object Windows.Controls.ProgressBar
    $script:Bar.Height = 18; $script:Bar.Background = '#070709'
    $script:Bar.Foreground = '#FF2E8B'; $script:Bar.Minimum = 0; $script:Bar.Maximum = 100
    $body.Children.Add($script:Bar) | Out-Null
    $script:Pct = T '0%' 12 '#FF6EB0'
    $body.Children.Add($script:Pct) | Out-Null
    $btnBack.IsEnabled = $false
    $btnNext.IsEnabled = $false
    $btnNext.Content = 'Please wait…'
}

function LogLine([string]$msg, [int]$pct) {
    $window.Dispatcher.Invoke({
        $script:Log.AppendText("> $msg`r`n")
        $script:Log.ScrollToEnd()
        $script:Now.Text = $msg
        $script:Bar.Value = $pct
        $script:Pct.Text = "$pct%"
    })
}

function Find-Python {
    foreach ($c in @('py -3', 'py', 'python', 'python3')) {
        try {
            $v = & cmd.exe /c "$c --version 2>&1"
            if ($LASTEXITCODE -eq 0 -and "$v" -match 'Python 3\.(\d+)') {
                if ([int]$Matches[1] -ge 10) { return $c }
            }
        } catch {}
    }
    return $null
}

function Start-Unpack {
    $script:Busy = $true
    $script:Py = Find-Python
    if (-not $script:Py) {
        $winget = Get-Command winget -ErrorAction SilentlyContinue
        if ($winget) {
            LogLine 'Python missing — winget Python 3.12…' 5
            try { winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements | Out-Null } catch {}
            $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
            $script:Py = Find-Python
        }
    }
    if (-not $script:Py) {
        Start-Process 'https://www.python.org/downloads/'
        [System.Windows.MessageBox]::Show("Installe Python 3.12 (coche Add python.exe to PATH) puis relance INSTALLER.bat.", "Bone Setup") | Out-Null
        $window.Close(); return
    }
    LogLine "Found $($script:Py)" 8
    LogLine 'Extracting: persona.json' 15
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    Copy-Item -Path (Join-Path $Payload '*') -Destination $InstallDir -Recurse -Force
    LogLine 'Extracting: discord_bot.py / llm.py' 28
    $venvPy = Join-Path $InstallDir '.venv\Scripts\python.exe'
    if (-not (Test-Path $venvPy)) {
        LogLine 'Creating venv…' 36
        & cmd.exe /c "$script:Py -m venv `"$InstallDir\.venv`""
        if ($LASTEXITCODE -ne 0) { throw 'venv failed' }
    }
    LogLine 'Installing discord.py-2.4.0' 55
    & $venvPy -m pip install -q --upgrade pip
    LogLine 'Installing python-dotenv' 70
    & $venvPy -m pip install -q -r (Join-Path $InstallDir 'requirements.txt')
    if ($LASTEXITCODE -ne 0) { throw 'pip failed' }
    LogLine 'Writing shortcuts…' 88
    Write-Launchers
    LogLine 'Done. Bone unpacked.' 100
    $script:Busy = $false
    $window.Dispatcher.Invoke({ $btnNext.IsEnabled = $true; $btnNext.Content = 'Next >' })
}

function Write-Launchers {
    $demarrer = "@echo off`r`ncd /d `"%LOCALAPPDATA%\Bone`"`r`nif exist ready.json del ready.json`r`nstart `"Bone`" /MIN `".venv\Scripts\python.exe`" discord_bot.py`r`n"
    $arreter = "@echo off`r`ncd /d `"%LOCALAPPDATA%\Bone`"`r`npowershell -NoProfile -Command `"Get-CimInstance Win32_Process | Where-Object { `$_.CommandLine -like '*discord_bot.py*' } | ForEach-Object { Stop-Process -Id `$_.ProcessId -Force -ErrorAction SilentlyContinue }`"`r`n"
    Set-Content (Join-Path $InstallDir 'demarrer.bat') $demarrer -Encoding ASCII
    Set-Content (Join-Path $InstallDir 'arreter.bat') $arreter -Encoding ASCII
    $w = New-Object -ComObject WScript.Shell
    $ico = Join-Path $InstallDir 'assets\bone.ico'
    if (-not (Test-Path $ico)) { $ico = Join-Path $InstallDir 'assets\bone.png' }
    $desktop = [Environment]::GetFolderPath('Desktop')
    $startDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Bone'
    New-Item -ItemType Directory -Force -Path $startDir | Out-Null
    function Lnk($path, $target) {
        $s = $w.CreateShortcut($path); $s.TargetPath = $target; $s.WorkingDirectory = $InstallDir
        if (Test-Path $ico) { $s.IconLocation = $ico }; $s.Save()
    }
    if ($script:ChkDesk.IsChecked) { Lnk (Join-Path $desktop 'Bone.lnk') (Join-Path $InstallDir 'demarrer.bat') }
    if ($script:ChkStart.IsChecked) {
        Lnk (Join-Path $startDir 'Bone.lnk') (Join-Path $InstallDir 'demarrer.bat')
        Lnk (Join-Path $startDir 'Arreter Bone.lnk') (Join-Path $InstallDir 'arreter.bat')
        $auth = Join-Path $InstallDir 'autorisations.bat'
        if (Test-Path $auth) { Lnk (Join-Path $startDir 'Bone autorisations.lnk') $auth }
    }
    if ($script:ChkBoot.IsChecked) {
        $startup = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
        Lnk (Join-Path $startup 'Bone.lnk') (Join-Path $InstallDir 'demarrer.bat')
    }
}

function Show-Token {
    Clear-Body
    $body.Children.Add((T 'Discord application')) | Out-Null
    $body.Children.Add((T "Une seule fois. New Application → Bone → Bot → Add Bot → MESSAGE CONTENT INTENT ON → Reset Token → Copy." 14 '#9A8894')) | Out-Null
    $link = New-Object Windows.Controls.Button
    $link.Content = 'Open Developer Portal'; $link.Margin = '0,8,0,12'; $link.Height = 32; $link.Width = 220
    $link.HorizontalAlignment = 'Left'
    $link.Add_Click({ Start-Process $Portal })
    $body.Children.Add($link) | Out-Null
    $script:TokBox = New-Object Windows.Controls.PasswordBox
    $script:TokBox.Height = 34; $script:TokBox.FontSize = 14
    $body.Children.Add($script:TokBox) | Out-Null
    $btnBack.IsEnabled = $false
    PinkNext 'Verify token'
}

function Show-Server {
    Clear-Body
    $body.Children.Add((T 'Choose your Discord server')) | Out-Null
    $body.Children.Add((T "Une fenetre Discord s'ouvre. Choisis Olympus (ou un autre) puis Autoriser." 14 '#9A8894')) | Out-Null
    $script:GuildTxt = T '' 16 '#3EE0A0'
    $body.Children.Add($script:GuildTxt) | Out-Null
    $btnBack.IsEnabled = $false
    PinkNext 'Open Discord'
}

function Show-Done([string]$guilds) {
    Clear-Body
    $body.Children.Add((T 'Setup complete')) | Out-Null
    $body.Children.Add((T 'Bone is installed.' 18 '#3EE0A0')) | Out-Null
    if ($guilds) { $body.Children.Add((T "Serveur : $guilds" 14 '#FF6EB0')) | Out-Null }
    $body.Children.Add((T 'Dans Discord : @Bone salut   /roast   /autorisations' 14 '#9A8894')) | Out-Null
    $btnBack.IsEnabled = $false
    PinkNext 'Finish'
}

function Go-Next {
    if ($script:Busy) { return }
    switch ($script:Page) {
        0 { $script:Page = 1; Show-Options }
        1 {
            $script:Page = 2; Show-Install
            $window.Dispatcher.BeginInvoke([action]{ try { Start-Unpack } catch {
                [System.Windows.MessageBox]::Show("$_", "Bone Setup") | Out-Null
            }}) | Out-Null
        }
        2 { $script:Page = 3; Show-Token }
        3 {
            $script:Token = $script:TokBox.Password.Trim()
            if ($script:Token.Length -lt 20) {
                [System.Windows.MessageBox]::Show("Token trop court. Reset Token → Copy.", "Bone Setup") | Out-Null
                return
            }
            try {
                $me = Invoke-RestMethod -Uri 'https://discord.com/api/v10/users/@me' -Headers @{ Authorization = "Bot $($script:Token)" }
            } catch {
                [System.Windows.MessageBox]::Show("Token refuse par Discord.", "Bone Setup") | Out-Null
                return
            }
            $script:ClientId = [string]$me.id
            @"
DISCORD_TOKEN=$($script:Token)
BONE_GUILD=Olympus
BONE_CHATTY=1
BONE_CHANNELS=général,general,olympus,bone,chat,lounge,accueil,welcome
BONE_LLM=auto
"@ | Set-Content (Join-Path $InstallDir '.env') -Encoding UTF8
            $script:Page = 4; Show-Server
        }
        4 {
            $invite = "https://discord.com/oauth2/authorize?client_id=$($script:ClientId)&permissions=$Perms&scope=bot%20applications.commands"
            Start-Process $invite
            $venvPy = Join-Path $InstallDir '.venv\Scripts\python.exe'
            Remove-Item (Join-Path $InstallDir 'ready.json') -ErrorAction SilentlyContinue
            Start-Process -FilePath $venvPy -ArgumentList 'discord_bot.py' -WorkingDirectory $InstallDir -WindowStyle Minimized
            $ready = $null
            for ($n = 0; $n -lt 40; $n++) {
                Start-Sleep -Milliseconds 400
                $rp = Join-Path $InstallDir 'ready.json'
                if (Test-Path $rp) { try { $ready = Get-Content $rp -Raw -Encoding UTF8 | ConvertFrom-Json } catch {} }
                if ($ready) { break }
            }
            $names = ''
            if ($ready -and $ready.guilds) { $names = ($ready.guilds | ForEach-Object { $_.name }) -join ', ' }
            if (-not $names) { $script:GuildTxt.Text = "Autorise le serveur, puis Finish." }
            else { $script:GuildTxt.Text = "OK  $names" }
            $script:Page = 5
            Show-Done $names
        }
        5 { $window.Close() }
    }
}

$btnNext.Add_Click({ Go-Next })
$btnBack.Add_Click({ if ($script:Page -eq 1) { $script:Page = 0; Show-Welcome } })
$btnCancel.Add_Click({ $window.Close() })
Show-Welcome
[void]$window.ShowDialog()
exit 0
