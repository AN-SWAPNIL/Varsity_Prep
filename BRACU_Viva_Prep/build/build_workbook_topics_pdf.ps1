[CmdletBinding()]
param([ValidateSet('BRACU','UIU')][string]$Pack='BRACU')
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$workspaceRoot=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$packRoot=Join-Path $workspaceRoot ($Pack+'_Viva_Prep')
$stem=$Pack+'_Seniors_Workbook_Topics_Explained'
$source=Join-Path $packRoot ($stem+'.md')
if (-not (Test-Path -LiteralPath $source)) { throw 'Run assemble_workbook_topics.py first.' }
$workRoot=Join-Path $packRoot 'build\workbook_topics'
$renderRoot=Join-Path $workRoot ('render-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $renderRoot -Force | Out-Null
$combined=Join-Path $renderRoot 'combined.md'
$html=Join-Path $renderRoot 'topics.html'
$rawPdf=Join-Path $renderRoot 'chrome.pdf'
$processed=Join-Path $renderRoot 'processed.pdf'
Copy-Item -LiteralPath $source -Destination $combined
& python (Join-Path $PSScriptRoot 'render_mermaid.py') $combined (Join-Path $renderRoot 'diagrams')
if ($LASTEXITCODE -ne 0) { throw 'Mermaid rendering failed.' }
$reader='markdown-yaml_metadata_block-simple_tables-multiline_tables-grid_tables+tex_math_dollars+tex_math_single_backslash+raw_html+fenced_divs+link_attributes'
$pandoc=Get-Command pandoc -ErrorAction SilentlyContinue
$pandocPrefix=@()
if ($pandoc) { $pandocExecutable=$pandoc.Source }
else {
    $pandocExecutable='D:\Applications\Quarto\bin\quarto.exe'
    if (-not (Test-Path -LiteralPath $pandocExecutable)) { throw 'Pandoc and the installed Quarto fallback were not found.' }
    $pandocPrefix=@('pandoc')
}
& $pandocExecutable @pandocPrefix $combined --from=$reader --to=html5 --standalone --embed-resources --mathml --toc --toc-depth=2 `
    "--metadata=title=Bismillah. $Pack - Seniors' Workbook Topics Explained" `
    '--metadata=author=Ahmmad Nur Swapnil' `
    "--css=$(Join-Path $packRoot 'build\viva-dark.css')" `
    "--resource-path=$renderRoot;$packRoot;$workspaceRoot\BRACU_Viva_Prep" --output=$html
if ($LASTEXITCODE -ne 0) { throw 'Pandoc conversion failed.' }
$htmlText=[IO.File]::ReadAllText($html)
if ($htmlText.Contains('<merror') -or $htmlText.Contains('<td>###')) { throw 'Math or table rendering error in generated HTML.' }
$browser=@('C:\Program Files\Microsoft\Edge\Application\msedge.exe',
           'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
           'C:\Program Files\Google\Chrome\Application\chrome.exe') |
    Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $browser) { throw 'Chrome/Edge not found.' }
$browserArgs=@('--headless=new','--disable-gpu','--disable-extensions','--disable-dev-shm-usage',
 '--allow-file-access-from-files','--run-all-compositor-stages-before-draw','--virtual-time-budget=8000',
 '--no-first-run','--no-pdf-header-footer',"--user-data-dir=$(Join-Path $renderRoot 'browser-profile')",
 "--print-to-pdf=$rawPdf",([Uri]([IO.Path]::GetFullPath($html))).AbsoluteUri)
$process=Start-Process -FilePath $browser -ArgumentList $browserArgs -Wait -PassThru -WindowStyle Hidden
if ($process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $rawPdf)) { throw 'Browser PDF generation failed.' }
& python (Join-Path $PSScriptRoot 'finish_workbook_topics_pdf.py') $rawPdf $processed $source $workRoot
if ($LASTEXITCODE -ne 0) { throw 'PDF verification failed; final output left unchanged.' }
$final=Join-Path $packRoot ($stem+'.pdf')
Move-Item -LiteralPath $processed -Destination $final -Force
Write-Output "Built: $final"
# Keep intermediate HTML and diagrams for inspection. No original files deleted.
