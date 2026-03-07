Add-Type -AssemblyName System.Drawing

$width = 1400
$height = 900
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$pen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 3)
$brush = [System.Drawing.Brushes]::Black

$fontTitle = New-Object System.Drawing.Font('Times New Roman', 28, [System.Drawing.FontStyle]::Bold)
$fontMain = New-Object System.Drawing.Font('Times New Roman', 22, [System.Drawing.FontStyle]::Bold)
$fontLabel = New-Object System.Drawing.Font('Times New Roman', 14, [System.Drawing.FontStyle]::Bold)

# Arrow-cap pen
$arrowPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 3)
$cap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(6, 8)
$arrowPen.CustomEndCap = $cap

function Draw-CenteredText {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [System.Drawing.Font]$Font,
        [System.Drawing.RectangleF]$Rect
    )
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $Graphics.DrawString($Text, $Font, [System.Drawing.Brushes]::Black, $Rect, $sf)
}

# Title
$g.DrawString('Context Flow Diagram - Crown Finance', $fontTitle, $brush, 360, 25)

# External entity boxes
$userRect = New-Object System.Drawing.RectangleF(90, 350, 250, 120)
$adminRect = New-Object System.Drawing.RectangleF(1060, 350, 250, 120)
$aiRect = New-Object System.Drawing.RectangleF(1020, 90, 290, 120)

$g.DrawRectangle($pen, $userRect.X, $userRect.Y, $userRect.Width, $userRect.Height)
$g.DrawRectangle($pen, $adminRect.X, $adminRect.Y, $adminRect.Width, $adminRect.Height)
$g.DrawRectangle($pen, $aiRect.X, $aiRect.Y, $aiRect.Width, $aiRect.Height)

Draw-CenteredText -Graphics $g -Text 'User' -Font $fontMain -Rect $userRect
Draw-CenteredText -Graphics $g -Text 'Admin' -Font $fontMain -Rect $adminRect
Draw-CenteredText -Graphics $g -Text 'AI Engine' -Font $fontMain -Rect $aiRect

# Central process circle
$centerX = 700
$centerY = 430
$radius = 150
$g.DrawEllipse($pen, $centerX - $radius, $centerY - $radius, $radius * 2, $radius * 2)
$procRect = New-Object System.Drawing.RectangleF ([single]($centerX - $radius)), ([single]($centerY - $radius)), ([single]($radius * 2)), ([single]($radius * 2))
$procFont = New-Object System.Drawing.Font('Times New Roman', 30, [System.Drawing.FontStyle]::Bold)
Draw-CenteredText -Graphics $g -Text "Crown`nFinance" -Font $procFont -Rect $procRect

# Database cylinder
$dbX = 560
$dbY = 650
$dbW = 280
$dbH = 180
$ovalH = 34
$g.DrawEllipse($pen, $dbX, $dbY - $ovalH, $dbW, $ovalH * 2)
$g.DrawRectangle($pen, $dbX, $dbY, $dbW, $dbH)
$g.DrawEllipse($pen, $dbX, $dbY + $dbH - $ovalH, $dbW, $ovalH * 2)
$dbRect = New-Object System.Drawing.RectangleF ([single]$dbX), ([single]($dbY + 20)), ([single]$dbW), ([single]($dbH - 20))
$dbFont = New-Object System.Drawing.Font('Times New Roman', 22, [System.Drawing.FontStyle]::Bold)
Draw-CenteredText -Graphics $g -Text "Finance`nDatabase" -Font $dbFont -Rect $dbRect

# Flows
$g.DrawLine($arrowPen, 340, 390, 550, 400)
$g.DrawString('Register/Login, Add transactions', $fontLabel, $brush, 350, 340)

$g.DrawLine($arrowPen, 550, 470, 340, 460)
$g.DrawString('View dashboard, reports', $fontLabel, $brush, 370, 485)

$g.DrawLine($arrowPen, 1060, 400, 850, 410)
$g.DrawString('Manage users, settings', $fontLabel, $brush, 885, 355)

$g.DrawLine($arrowPen, 850, 475, 1060, 470)
$g.DrawString('View system reports', $fontLabel, $brush, 890, 490)

$g.DrawLine($arrowPen, 1020, 210, 820, 320)
$g.DrawString('Send insight request', $fontLabel, $brush, 830, 235)

$g.DrawLine($arrowPen, 820, 340, 1020, 130)
$g.DrawString('Receive AI suggestions', $fontLabel, $brush, 815, 165)

$g.DrawLine($arrowPen, 670, 580, 670, 650)
$g.DrawString('Store data', $fontLabel, $brush, 555, 600)

$g.DrawLine($arrowPen, 730, 650, 730, 580)
$g.DrawString('Retrieve data', $fontLabel, $brush, 745, 600)

# Save file
if (-not (Test-Path 'image')) {
    New-Item -ItemType Directory -Path 'image' | Out-Null
}

$outFile = 'image/crown_finance_context_flow.png'
$bmp.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)

$g.Dispose()
$bmp.Dispose()
$pen.Dispose()
$arrowPen.Dispose()
$fontTitle.Dispose()
$fontMain.Dispose()
$fontLabel.Dispose()
$procFont.Dispose()
$dbFont.Dispose()

Write-Output "Saved: $outFile"
