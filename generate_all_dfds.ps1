Add-Type -AssemblyName System.Drawing

function New-DFDImage {
    param(
        [int]$Width = 1600,
        [int]$Height = 1000,
        [string]$Title = "Data Flow Diagram"
    )
    
    $bmp = New-Object System.Drawing.Bitmap($Width, $Height)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.Clear([System.Drawing.Color]::White)
    
    # Title
    $fontTitle = New-Object System.Drawing.Font('Arial', 24, [System.Drawing.FontStyle]::Bold)
    $titleSize = $g.MeasureString($Title, $fontTitle)
    $g.DrawString($Title, $fontTitle, [System.Drawing.Brushes]::Black, ($Width - $titleSize.Width) / 2, 20)
    $fontTitle.Dispose()
    
    return @{Graphics = $g; Bitmap = $bmp}
}

function Draw-Process {
    param(
        [System.Drawing.Graphics]$g,
        [float]$x,
        [float]$y,
        [float]$w,
        [float]$h,
        [string]$text,
        [string]$number = ""
    )
    
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 3)
    $g.DrawEllipse($pen, $x, $y, $w, $h)
    $pen.Dispose()
    
    $font = New-Object System.Drawing.Font('Arial', 16, [System.Drawing.FontStyle]::Bold)
    $rect = New-Object System.Drawing.RectangleF($x, $y, $w, $h)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    
    if ($number) {
        $g.DrawString("$number`n$text", $font, [System.Drawing.Brushes]::Black, $rect, $sf)
    } else {
        $g.DrawString($text, $font, [System.Drawing.Brushes]::Black, $rect, $sf)
    }
    
    $font.Dispose()
    $sf.Dispose()
}

function Draw-Entity {
    param(
        [System.Drawing.Graphics]$g,
        [float]$x,
        [float]$y,
        [float]$w,
        [float]$h,
        [string]$text
    )
    
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 3)
    $g.DrawRectangle($pen, $x, $y, $w, $h)
    $pen.Dispose()
    
    $font = New-Object System.Drawing.Font('Arial', 14, [System.Drawing.FontStyle]::Bold)
    $rect = New-Object System.Drawing.RectangleF($x, $y, $w, $h)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $g.DrawString($text, $font, [System.Drawing.Brushes]::Black, $rect, $sf)
    
    $font.Dispose()
    $sf.Dispose()
}

function Draw-DataStore {
    param(
        [System.Drawing.Graphics]$g,
        [float]$x,
        [float]$y,
        [float]$w,
        [float]$h,
        [string]$text,
        [string]$number = ""
    )
    
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 3)
    $x1 = [float]$x
    $y1 = [float]$y
    $w1 = [float]$w
    $h1 = [float]$h
    
    # Draw all 4 sides for complete rectangle
    $g.DrawLine($pen, $x1, $y1, $x1 + $w1, $y1)              # Top
    $g.DrawLine($pen, $x1, $y1 + $h1, $x1 + $w1, $y1 + $h1)  # Bottom
    $g.DrawLine($pen, $x1, $y1, $x1, $y1 + $h1)              # Left
    $g.DrawLine($pen, $x1 + $w1, $y1, $x1 + $w1, $y1 + $h1)  # Right
    $pen.Dispose()
    
    $font = New-Object System.Drawing.Font('Arial', 13, [System.Drawing.FontStyle]::Bold)
    $rect = New-Object System.Drawing.RectangleF([single]($x1 + 5), [single]$y1, [single]($w1 - 10), [single]$h1)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    
    if ($number) {
        $displayText = "$number  $text"
        $g.DrawString($displayText, $font, [System.Drawing.Brushes]::Black, $rect, $sf)
    } else {
        $g.DrawString($text, $font, [System.Drawing.Brushes]::Black, $rect, $sf)
    }
    
    $font.Dispose()
    $sf.Dispose()
}

function Draw-Arrow {
    param(
        [System.Drawing.Graphics]$g,
        [float]$x1,
        [float]$y1,
        [float]$x2,
        [float]$y2,
        [string]$label = ""
    )
    
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 2)
    $cap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(5, 6)
    $pen.CustomEndCap = $cap
    
    $g.DrawLine($pen, $x1, $y1, $x2, $y2)
    $pen.Dispose()
    
    if ($label) {
        $font = New-Object System.Drawing.Font('Arial', 11)
        $mx = ($x1 + $x2) / 2
        $my = ($y1 + $y2) / 2
        $size = $g.MeasureString($label, $font)
        $g.FillRectangle([System.Drawing.Brushes]::White, $mx - $size.Width/2 - 3, $my - $size.Height/2 - 2, $size.Width + 6, $size.Height + 4)
        $g.DrawString($label, $font, [System.Drawing.Brushes]::Black, $mx - $size.Width/2, $my - $size.Height/2)
        $font.Dispose()
    }
}

function Save-Image {
    param(
        $ImageData,
        [string]$FileName
    )
    
    $outPath = "image/$FileName"
    $ImageData.Bitmap.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $ImageData.Graphics.Dispose()
    $ImageData.Bitmap.Dispose()
    Write-Output "Generated: $outPath"
}

# Create image folder
if (-not (Test-Path 'image')) {
    New-Item -ItemType Directory -Path 'image' | Out-Null
}

# ============== DFD Level-0 ==============
Write-Output "Generating DFD Level-0..."
$img = New-DFDImage -Width 1400 -Height 900 -Title "DFD Level-0 - Crown Finance System"

Draw-Entity $img.Graphics 80 380 220 100 "User"
Draw-Entity $img.Graphics 1100 380 220 100 "Admin"
Draw-Entity $img.Graphics 1050 150 270 90 "AI/ML Engine"

Draw-Process $img.Graphics 550 350 300 200 "Crown Finance`nSystem" "0"

Draw-DataStore $img.Graphics 500 650 400 60 "Financial Database" "D1"

Draw-Arrow $img.Graphics 300 420 550 420 "User requests"
Draw-Arrow $img.Graphics 550 460 300 450 "Reports/Insights"
Draw-Arrow $img.Graphics 1100 420 850 420 "Admin commands"
Draw-Arrow $img.Graphics 850 450 1100 440 "System reports"
Draw-Arrow $img.Graphics 1050 210 820 360 "Data for analysis"
Draw-Arrow $img.Graphics 800 370 1050 200 "AI predictions"
Draw-Arrow $img.Graphics 680 550 680 650 "Store data"
Draw-Arrow $img.Graphics 720 650 720 550 "Retrieve data"

Save-Image $img "dfd_level_0.png"

# ============== DFD Level-1 ==============
Write-Output "Generating DFD Level-1..."
$img = New-DFDImage -Width 1600 -Height 1100 -Title "DFD Level-1 - Crown Finance System Decomposition"

Draw-Entity $img.Graphics 50 200 200 80 "User"
Draw-Entity $img.Graphics 1350 200 200 80 "Admin"

Draw-Process $img.Graphics 350 150 220 100 "User`nAuthentication" "1"
Draw-Process $img.Graphics 700 150 220 100 "Transaction`nManagement" "2"
Draw-Process $img.Graphics 1050 150 220 100 "Budget &`nGoals" "3"
Draw-Process $img.Graphics 500 450 220 100 "Analytics`nEngine" "4"
Draw-Process $img.Graphics 900 450 220 100 "AI Insight`nGenerator" "5"

Draw-DataStore $img.Graphics 300 650 250 50 "User Accounts" "D1"
Draw-DataStore $img.Graphics 600 650 250 50 "Transactions" "D2"
Draw-DataStore $img.Graphics 900 650 250 50 "Budgets/Goals" "D3"
Draw-DataStore $img.Graphics 450 800 350 50 "Analytics Data" "D4"

Draw-Arrow $img.Graphics 250 230 350 190 "Login/Signup"
Draw-Arrow $img.Graphics 570 190 700 190 "Auth token"
Draw-Arrow $img.Graphics 920 190 1050 190 "Budget request"
Draw-Arrow $img.Graphics 1270 220 1350 230 "Admin access"
Draw-Arrow $img.Graphics 460 250 500 450 "User data"
Draw-Arrow $img.Graphics 810 250 900 450 "Transaction data"
Draw-Arrow $img.Graphics 600 550 600 650 "Store trans."
Draw-Arrow $img.Graphics 425 650 425 550 "Fetch user"
Draw-Arrow $img.Graphics 725 650 720 550 "Read trans."
Draw-Arrow $img.Graphics 1010 550 1010 650 "Store goals"
Draw-Arrow $img.Graphics 1040 650 1040 550 "Fetch goals"
Draw-Arrow $img.Graphics 625 800 610 550 "Analytics results"

Save-Image $img "dfd_level_1.png"

# ============== DFD Level-2.1 (Authentication) ==============
Write-Output "Generating DFD Level-2.1..."
$img = New-DFDImage -Width 1400 -Height 950 -Title "DFD Level-2.1 - User Authentication Module"

Draw-Entity $img.Graphics 100 350 200 80 "User"

Draw-Process $img.Graphics 450 200 200 90 "Validate`nCredentials" "1.1"
Draw-Process $img.Graphics 850 200 200 90 "Generate`nJWT Token" "1.2"
Draw-Process $img.Graphics 450 450 200 90 "Create New`nAccount" "1.3"
Draw-Process $img.Graphics 850 450 200 90 "Update`nProfile" "1.4"

Draw-DataStore $img.Graphics 550 650 300 60 "User Database" "D1"

Draw-Arrow $img.Graphics 300 380 450 240 "Login request"
Draw-Arrow $img.Graphics 650 240 850 240 "Valid user"
Draw-Arrow $img.Graphics 950 290 950 350 "JWT token"
Draw-Arrow $img.Graphics 950 350 300 390 "Auth token"
Draw-Arrow $img.Graphics 300 405 450 480 "Signup data"
Draw-Arrow $img.Graphics 550 540 600 650 "New user data"
Draw-Arrow $img.Graphics 550 290 630 650 "Read user"
Draw-Arrow $img.Graphics 750 650 850 540 "User info"
Draw-Arrow $img.Graphics 300 415 850 480 "Update request"

Save-Image $img "dfd_level_2_1.png"

# ============== DFD Level-2.2 (Transaction Management) ==============
Write-Output "Generating DFD Level-2.2..."
$img = New-DFDImage -Width 1500 -Height 1000 -Title "DFD Level-2.2 - Transaction Management Module"

Draw-Entity $img.Graphics 100 400 200 80 "User"

Draw-Process $img.Graphics 450 200 220 90 "Add/Edit`nTransaction" "2.1"
Draw-Process $img.Graphics 850 200 220 90 "Categorize`nExpense" "2.2"
Draw-Process $img.Graphics 1150 350 220 90 "Calculate`nTotals" "2.3"
Draw-Process $img.Graphics 450 500 220 90 "Filter &`nSearch" "2.4"
Draw-Process $img.Graphics 850 500 220 90 "Export`nData" "2.5"

Draw-DataStore $img.Graphics 550 750 350 60 "Transaction Database" "D2"
Draw-DataStore $img.Graphics 550 870 350 60 "Category Master" "D5"

Draw-Arrow $img.Graphics 300 430 450 245 "New transaction"
Draw-Arrow $img.Graphics 670 240 850 240 "Transaction data"
Draw-Arrow $img.Graphics 1070 245 1150 380 "Categorized data"
Draw-Arrow $img.Graphics 1370 395 1370 440 ""
Draw-Arrow $img.Graphics 1370 440 300 460 "Summary"
Draw-Arrow $img.Graphics 300 455 450 530 "Search query"
Draw-Arrow $img.Graphics 670 540 850 540 "Filtered data"
Draw-Arrow $img.Graphics 1070 540 1100 540 "Export request"
Draw-Arrow $img.Graphics 560 290 650 750 "Save trans."
Draw-Arrow $img.Graphics 750 750 750 590 "Read trans."
Draw-Arrow $img.Graphics 850 590 800 870 "Categories"

Save-Image $img "dfd_level_2_2.png"

# ============== DFD Level-2.3 (Budget & Goals) ==============
Write-Output "Generating DFD Level-2.3..."
$img = New-DFDImage -Width 1500 -Height 1000 -Title "DFD Level-2.3 - Budget & Goals Management Module"

Draw-Entity $img.Graphics 100 400 200 80 "User"

Draw-Process $img.Graphics 450 180 220 90 "Set Budget`nLimits" "3.1"
Draw-Process $img.Graphics 850 180 220 90 "Track`nSpending" "3.2"
Draw-Process $img.Graphics 1150 350 220 90 "Calculate`nProgress" "3.3"
Draw-Process $img.Graphics 450 500 220 90 "Set Financial`nGoals" "3.4"
Draw-Process $img.Graphics 850 500 220 90 "Monitor`nGoals" "3.5"

Draw-DataStore $img.Graphics 550 730 350 60 "Budget Database" "D3"
Draw-DataStore $img.Graphics 550 850 350 60 "Goals Database" "D6"
Draw-DataStore $img.Graphics 1050 650 300 60 "Transaction Data" "D2"

Draw-Arrow $img.Graphics 300 430 450 215 "Budget input"
Draw-Arrow $img.Graphics 670 215 850 215 "Budget limits"
Draw-Arrow $img.Graphics 1070 225 1150 380 "Expense data"
Draw-Arrow $img.Graphics 1350 670 1260 440 "Spending vs budget"
Draw-Arrow $img.Graphics 1260 395 300 445 "Alerts/Reports"
Draw-Arrow $img.Graphics 300 455 450 530 "Goal details"
Draw-Arrow $img.Graphics 670 540 850 540 "Goal targets"
Draw-Arrow $img.Graphics 550 270 650 730 "Save budget"
Draw-Arrow $img.Graphics 750 730 850 270 "Read budget"
Draw-Arrow $img.Graphics 550 590 650 850 "Store goals"
Draw-Arrow $img.Graphics 750 850 850 590 "Fetch goals"
Draw-Arrow $img.Graphics 1050 670 1010 270 "Read expenses"

Save-Image $img "dfd_level_2_3.png"

Write-Output "`nAll DFD diagrams generated successfully in 'image' folder!"
