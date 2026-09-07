[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$buildRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$packRoot = Split-Path -Parent $buildRoot
$outputName = 'UIU_CSE_Demo_and_Interview_Preparation_Ahmmad_Nur_Swapnil.pdf'
$finalOutput = Join-Path $packRoot $outputName
$generatedRoot = Join-Path $packRoot '.generated'

$sourceNames = @(
    'README.md',
    '00_UIU_DEMO_AND_QA_GUIDE.md',
    '04_C_PROGRAMMING_SLIDE_COMPLETE.md',
    '03_OOP_CPP_JAVA_SLIDE_COMPLETE.md',
    '10_DISCRETE_MATHEMATICS_SLIDE_COMPLETE.md',
    '01_DSA_I_SLIDE_COMPLETE.md',
    '02_DSA_II_SLIDE_COMPLETE.md',
    '05_DBMS_SLIDE_COMPLETE.md',
    '08_SOFTWARE_ENGINEERING_SLIDE_COMPLETE.md',
    '06_OPERATING_SYSTEMS_SLIDE_COMPLETE.md',
    '09_ARTIFICIAL_INTELLIGENCE_SLIDE_COMPLETE.md',
    '11_MACHINE_LEARNING_SLIDE_COMPLETE.md',
    '17_THESIS_RESEARCH_INDUSTRY_COMPLETE.md',
    '19_UIU_RELEVANT_COMMON_INTERVIEW_QA.md',
    '20_SENIORS_WORKBOOK_COVERAGE_AUDIT.md'
)

$sourcePaths = foreach ($name in $sourceNames) {
    $path = Join-Path $packRoot $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing source file: $path"
    }
    (Resolve-Path -LiteralPath $path).Path
}

foreach ($command in @('pandoc', 'python')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command is unavailable: $command"
    }
}

$chromeCandidates = @(
    'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
)
$chrome = $chromeCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
if (-not $chrome) {
    throw 'Chrome or Edge was not found for headless PDF rendering.'
}

$packFull = [IO.Path]::GetFullPath($packRoot).TrimEnd('\')
$generatedFull = [IO.Path]::GetFullPath($generatedRoot).TrimEnd('\')
if (-not $generatedFull.StartsWith($packFull + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to manage generated directory outside the pack: $generatedFull"
}
if (Test-Path -LiteralPath $generatedFull) {
    Remove-Item -LiteralPath $generatedFull -Recurse -Force
}
New-Item -ItemType Directory -Path $generatedFull | Out-Null

$combinedPath = Join-Path $generatedFull 'combined.md'
$htmlPath = Join-Path $generatedFull 'viva.html'
$chromePdf = Join-Path $generatedFull 'chrome.pdf'
$processedPdf = Join-Path $generatedFull 'processed.pdf'
$diagramRoot = Join-Path $generatedFull 'diagrams'
$browserProfile = Join-Path $generatedFull 'browser-profile'
$cssPath = Join-Path $buildRoot 'viva-dark.css'

$builder = [Text.StringBuilder]::new()
for ($index = 0; $index -lt $sourcePaths.Count; $index++) {
    if ($index -gt 0) {
        [void]$builder.AppendLine()
        [void]$builder.AppendLine('<div class="volume-break"></div>')
        [void]$builder.AppendLine()
    }
    [void]$builder.AppendLine("<!-- source: $($sourceNames[$index]) -->")
    [void]$builder.AppendLine([IO.File]::ReadAllText($sourcePaths[$index], [Text.Encoding]::UTF8))
    [void]$builder.AppendLine()
}
[IO.File]::WriteAllText($combinedPath, $builder.ToString(), [Text.UTF8Encoding]::new($false))

& python (Join-Path $buildRoot 'render_mermaid.py') $combinedPath $diagramRoot
if ($LASTEXITCODE -ne 0) {
    throw "Mermaid rendering failed with exit code $LASTEXITCODE"
}

# Disable Pandoc's whitespace-table extensions: horizontal rules adjacent to
# headings must not swallow entire chapters as narrow headerless tables.
# Pipe tables, fenced code, diagrams and mathematics remain enabled.
$reader = 'markdown-yaml_metadata_block-simple_tables-multiline_tables-grid_tables+tex_math_dollars+tex_math_single_backslash+raw_html+fenced_divs+link_attributes'
$resourcePath = "$generatedFull;$packFull"
& pandoc $combinedPath `
    --from=$reader `
    --to=html5 `
    --standalone `
    --embed-resources `
    --mathml `
    --toc `
    --toc-depth=3 `
    --metadata='title=Bismillah. UIU CSE Lecturer - Demo and Interview Preparation' `
    --metadata='author=Ahmmad Nur Swapnil' `
    "--css=$cssPath" `
    --resource-path=$resourcePath `
    --output=$htmlPath
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $htmlPath)) {
    throw "Pandoc HTML generation failed with exit code $LASTEXITCODE"
}

$htmlUri = ([Uri]([IO.Path]::GetFullPath($htmlPath))).AbsoluteUri
$chromeArguments = @(
    '--headless=new',
    '--disable-gpu',
    '--disable-extensions',
    '--disable-dev-shm-usage',
    '--allow-file-access-from-files',
    '--run-all-compositor-stages-before-draw',
    '--virtual-time-budget=8000',
    '--no-first-run',
    '--no-pdf-header-footer',
    "--user-data-dir=$browserProfile",
    "--print-to-pdf=$chromePdf",
    $htmlUri
)
$browserProcess = Start-Process -FilePath $chrome -ArgumentList $chromeArguments -Wait -PassThru -WindowStyle Hidden
if ($browserProcess.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $chromePdf)) {
    throw "Headless browser PDF generation failed with exit code $($browserProcess.ExitCode)"
}

$postArgs = @(
    (Join-Path $buildRoot 'postprocess_pdf.py'),
    '--input', $chromePdf,
    '--output', $processedPdf,
    '--markdown'
) + $sourcePaths
& python @postArgs
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $processedPdf)) {
    throw "PDF post-processing failed with exit code $LASTEXITCODE"
}

$verifiedOutput = [IO.Path]::GetFullPath($processedPdf)
if ((Get-Item -LiteralPath $verifiedOutput).Length -lt 1MB) {
    throw 'Generated PDF is unexpectedly small; refusing to replace the final output.'
}

Move-Item -LiteralPath $verifiedOutput -Destination $finalOutput -Force
Write-Output "Built: $finalOutput"

if (Test-Path -LiteralPath $generatedFull) {
    Remove-Item -LiteralPath $generatedFull -Recurse -Force
}
