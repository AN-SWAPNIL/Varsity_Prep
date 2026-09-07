$ErrorActionPreference = 'Stop'
$demoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$pptxPath = Join-Path $demoRoot 'sonia_np_completeness_demo_editable.pptx'
$previewRoot = Join-Path $PSScriptRoot 'editable\preview'
New-Item -ItemType Directory -Path $previewRoot -Force | Out-Null
$hadPowerPoint = @(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app = $null
$deck = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    # ReadOnly=true, Untitled=false, WithWindow=false: do not open a visible UI.
    $deck = $app.Presentations.Open($pptxPath, -1, 0, 0)
    $deck.Export($previewRoot, 'PNG', 1280, 960)
    $deck.SaveAs((Join-Path $demoRoot 'sonia_np_completeness_demo_editable.pdf'), 32)
    $issues = @()
    foreach ($slide in $deck.Slides) {
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $bound = $shape.TextFrame.TextRange.BoundHeight
                if ($bound -gt ($shape.Height + 3)) {
                    $issues += [pscustomobject]@{ Slide=$slide.SlideIndex; Shape=$shape.Name; Height=$shape.Height; TextHeight=$bound; Text=$shape.TextFrame.TextRange.Text.Substring(0,[Math]::Min(80,$shape.TextFrame.TextRange.Text.Length)) }
                }
            }
            if ($shape.Left -lt -2 -or $shape.Top -lt -2 -or ($shape.Left+$shape.Width) -gt ($deck.PageSetup.SlideWidth+2) -or ($shape.Top+$shape.Height) -gt ($deck.PageSetup.SlideHeight+2)) {
                $issues += [pscustomobject]@{ Slide=$slide.SlideIndex; Shape=$shape.Name; Issue='Outside slide bounds' }
            }
        }
    }
    $issues | ConvertTo-Json -Depth 4 | Write-Output
    Write-Output "PowerPoint rendered $($deck.Slides.Count) slides. Layout issues: $($issues.Count)."
} finally {
    if ($null -ne $deck) { $deck.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck) }
    if ($null -ne $app) {
        if (-not $hadPowerPoint) { $app.Quit() }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    }
}
