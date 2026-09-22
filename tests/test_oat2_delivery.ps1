$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
$notebookPath = Join-Path $repo "notebooks/oat2_pipeline_preditivo.ipynb"
$readmePath = Join-Path $repo "README.md"

$notebook = Get-Content -Raw -Encoding UTF8 $notebookPath | ConvertFrom-Json
$codigo = ($notebook.cells |
    Where-Object cell_type -eq "code" |
    ForEach-Object { $_.source -join "" }) -join "`n"
$markdown = ($notebook.cells |
    Where-Object cell_type -eq "markdown" |
    ForEach-Object { $_.source -join "" }) -join "`n"
$readme = Get-Content -Raw -Encoding UTF8 $readmePath

$falhas = [System.Collections.Generic.List[string]]::new()

function Exigir-Texto {
    param(
        [string]$Conteudo,
        [string]$Padrao,
        [string]$Mensagem
    )
    if ($Conteudo -notmatch $Padrao) {
        $falhas.Add($Mensagem)
    }
}

Exigir-Texto $codigo 'def\s+baseline_naive\s*\(' "Falta a função baseline_naive."
Exigir-Texto $codigo 'def\s+baseline_media_movel\s*\(' "Falta a função baseline_media_movel."
Exigir-Texto $codigo '\.shift\(1\)' "Falta deslocamento causal com shift(1)."
Exigir-Texto $codigo 'TimeSeriesSplit' "Falta validação temporal com TimeSeriesSplit."
Exigir-Texto $codigo 'mean_absolute_percentage_error' "Falta o cálculo de MAPE."
Exigir-Texto $codigo 'Resultados do Baseline\s*-\s*MAE:' "Falta o boletim no formato exigido."
Exigir-Texto $codigo 'lag_30' "Falta a feature lag_30 escolhida pela equipe."
Exigir-Texto $codigo 'head\(15\)' "Falta a validação df.head(15)."
Exigir-Texto $codigo 'Naive' "Falta a série Naive no gráfico comparativo."
Exigir-Texto $codigo 'baseline_media_movel\(serie,\s*janela=7\)' "Falta a media movel no grafico comparativo."
Exigir-Texto $markdown 'Decis.es da equipe' "Falta registrar as decisoes da equipe no notebook."
Exigir-Texto $readme 'OAT 2' "O README não identifica a entrega como OAT 2."
Exigir-Texto $readme 'oat2_pipeline_preditivo\.ipynb' "O README não aponta para o notebook OAT 2."
Exigir-Texto $readme 'lag_30' "O README não documenta o lag 30."

if ($falhas.Count -gt 0) {
    $falhas | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "OK: critérios estruturais da OAT 2 atendidos."
