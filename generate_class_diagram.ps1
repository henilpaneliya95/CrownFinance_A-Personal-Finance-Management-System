Add-Type -AssemblyName System.Drawing

$WIDTH = 1800
$HEIGHT = 1400
$bmp = New-Object System.Drawing.Bitmap($WIDTH, $HEIGHT)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$pen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 2)
$penThick = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 3)
$brush = [System.Drawing.Brushes]::Black
$brushLight = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(240, 240, 240))

$fontTitle = New-Object System.Drawing.Font('Arial', 18, [System.Drawing.FontStyle]::Bold)
$fontClass = New-Object System.Drawing.Font('Arial', 11, [System.Drawing.FontStyle]::Bold)
$fontAttr = New-Object System.Drawing.Font('Arial', 9)

# Title
$g.DrawString('Class Diagram - Crown Finance System', $fontTitle, $brush, 600, 15)

# Class Box Function
function Draw-ClassBox {
    param(
        [float]$x,
        [float]$y,
        [float]$width,
        [float]$height,
        [string]$classname,
        [string[]]$attributes,
        [string[]]$methods
    )
    
    $pen2 = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 2)
    
    # Main box
    $g.FillRectangle($brushLight, $x, $y, $width, $height)
    $g.DrawRectangle($pen2, $x, $y, $width, $height)
    
    # Class name section
    $nameHeight = 25
    $g.DrawLine($pen2, $x, $y + $nameHeight, $x + $width, $y + $nameHeight)
    $g.DrawString("«class»`n$classname", $fontClass, $brush, $x + 5, $y + 3)
    
    # Attributes section
    $attrY = $y + $nameHeight + 5
    $attrHeight = $attributes.Count * 14
    $g.DrawLine($pen2, $x, $attrY + $attrHeight, $x + $width, $attrY + $attrHeight)
    
    foreach ($attr in $attributes) {
        $g.DrawString("- $attr", $fontAttr, $brush, $x + 5, $attrY)
        $attrY += 14
    }
    
    # Methods section
    $methodY = $attrY + 5
    foreach ($method in $methods) {
        $g.DrawString("+ $method", $fontAttr, $brush, $x + 5, $methodY)
        $methodY += 14
    }
    
    $pen2.Dispose()
}

# Relationship arrow
function Draw-Relationship {
    param(
        [float]$x1,
        [float]$y1,
        [float]$x2,
        [float]$y2,
        [string]$label = "",
        [string]$type = "association"
    )
    
    $penRel = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 1.5)
    if ($type -eq "inheritance") {
        $penRel.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Solid
    }
    
    $g.DrawLine($penRel, $x1, $y1, $x2, $y2)
    $penRel.Dispose()
    
    if ($label) {
        $midX = ($x1 + $x2) / 2
        $midY = ($y1 + $y2) / 2
        $size = $g.MeasureString($label, $fontAttr)
        $g.FillRectangle([System.Drawing.Brushes]::White, $midX - $size.Width/2 - 2, $midY - $size.Height/2 - 2, $size.Width + 4, $size.Height + 4)
        $g.DrawString($label, $fontAttr, $brush, $midX - $size.Width/2, $midY - $size.Height/2)
    }
}

# Draw Classes

# Row 1 - Top Level
Draw-ClassBox 50 100 200 150 "User" @("user_id:int", "email:varchar", "password:varchar", "fullname:varchar", "status:varchar") @("login()", "registerUser()", "updateProfile()")

Draw-ClassBox 300 100 200 150 "Account" @("account_id:int", "user_id:int", "accounttype:varchar", "balance:float", "status:varchar") @("createAccount()", "getBalance()", "updateBalance()")

Draw-ClassBox 550 100 200 150 "Transaction" @("transaction_id:int", "account_id:int", "amount:float", "category_id:int", "status:varchar") @("addTransaction()", "editTransaction()", "getHistory()")

Draw-ClassBox 800 100 200 150 "Category" @("category_id:int", "categoryname:varchar", "categorytype:varchar", "status:varchar") @("addCategory()", "viewCategory()")

Draw-ClassBox 1050 100 200 150 "Budget" @("budget_id:int", "user_id:int", "budgetlimit:float", "spent:float", "status:varchar") @("createBudget()", "checkStatus()", "alert()")

# Row 2 - Middle
Draw-ClassBox 50 320 200 150 "Goal" @("goal_id:int", "user_id:int", "goalname:varchar", "target:float", "progress:float") @("createGoal()", "updateProgress()", "checkStatus()")

Draw-ClassBox 300 320 200 150 "Dashboard" @("dashboard_id:int", "user_id:int", "totalincome:float", "totalexpense:float", "balance:float") @("generateAnalytics()", "getCharts()", "getSummary()")

Draw-ClassBox 550 320 200 150 "Payment" @("payment_id:int", "user_id:int", "paymentmethod:varchar", "cardno:varchar", "status:varchar") @("addPaymentMethod()", "processPayment()", "validate()")

Draw-ClassBox 800 320 200 150 "Notification" @("notification_id:int", "user_id:int", "message:text", "notificationtype:varchar", "status:varchar") @("sendNotification()", "markRead()", "delete()")

# Row 3 - Bottom
Draw-ClassBox 50 540 200 150 "AIInsight" @("insight_id:int", "user_id:int", "insighttype:varchar", "recommendation:text", "score:float") @("generateInsight()", "analyzeSpending()", "suggest()")

Draw-ClassBox 300 540 200 150 "Report" @("report_id:int", "user_id:int", "reporttype:varchar", "startdate:date", "status:varchar") @("generateReport()", "exportReport()", "download()")

Draw-ClassBox 550 540 200 150 "UserProfile" @("profile_id:int", "user_id:int", "firstname:varchar", "address:text", "status:varchar") @("updateProfile()", "uploadPic()", "viewProfile()")

Draw-ClassBox 800 540 200 150 "Feedback" @("feedback_id:int", "user_id:int", "message:text", "rating:int", "status:varchar") @("submitFeedback()", "rateFeedback()", "respond()")

# Draw Relationships
# User relationships
Draw-Relationship 150 250 150 320 "1..*" "association"
Draw-Relationship 150 250 350 320 "1..*" "association"
Draw-Relationship 150 250 100 540 "1..*" "association"

# Account to Transaction
Draw-Relationship 400 250 650 250 "1..*" "association"

# Transaction to Category
Draw-Relationship 750 250 850 250 "*.1" "association"

# Account to Budget
Draw-Relationship 500 250 1100 250 "1..*" "association"

# User to Dashboard
Draw-Relationship 250 175 300 400 "1..1" "association"

# User to Payment
Draw-Relationship 250 175 550 400 "1..*" "association"

# Dashboard to Report
Draw-Relationship 400 475 350 540 "generates" "association"

# User to Profile
Draw-Relationship 150 250 600 540 "has" "association"

# User to Notification
Draw-Relationship 200 175 800 400 "receives" "association"

# User to Feedback
Draw-Relationship 150 250 800 540 "provides" "association"

# User to AIInsight
Draw-Relationship 150 250 100 540 "receives" "association"

# Legend
$fontBold = New-Object System.Drawing.Font('Arial', 10, [System.Drawing.FontStyle]::Bold)
$legendY = 750
$g.DrawString("Relationships:", $fontBold, $brush, 50, $legendY)
$g.DrawString("1..* = One to Many", $fontAttr, $brush, 50, $legendY + 25)
$g.DrawString("*.1 = Many to One", $fontAttr, $brush, 50, $legendY + 40)
$g.DrawString("1..1 = One to One", $fontAttr, $brush, 50, $legendY + 55)

# Notes
$noteY = $legendY + 100
$g.DrawString("Notes:", $fontBold, $brush, 50, $noteY)
$g.DrawString("All classes contain primary key (ID) and status fields for tracking.", $fontAttr, $brush, 50, $noteY + 25)
$g.DrawString("Methods shown are primary operations; additional utility methods may exist.", $fontAttr, $brush, 50, $noteY + 40)
$g.DrawString("User is the central entity connecting to most other classes.", $fontAttr, $brush, 50, $noteY + 55)

$fontBold.Dispose()

# Save
$outPath = "image/crown_finance_class_diagram.png"
$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)

$g.Dispose()
$bmp.Dispose()
$pen.Dispose()
$penThick.Dispose()

Write-Output "Saved: $outPath"
