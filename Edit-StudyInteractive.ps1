function Edit-StudyInteractive {
    do {
        Clear-Host
        # Listar estudos disponíveis
        $studies = Invoke-RestMethod -Uri "http://localhost:8000/studies/" -Method Get
        
        Write-Host "`n=== EDITOR DE ESTUDOS ===" -ForegroundColor Cyan
        Write-Host "`nEstudos disponíveis:" -ForegroundColor Cyan
        $studies | ForEach-Object { Write-Host "- $_" }
        Write-Host "`nOpções:" -ForegroundColor Yellow
        Write-Host "1. Editar um estudo"
        Write-Host "2. Verificar um estudo"
        Write-Host "3. Deletar um estudo"
        Write-Host "4. Adicionar novo estudo (JSON)"
        Write-Host "5. Sair"
        
        $option = Read-Host "`nEscolha uma opção (1-5)"
        
        switch ($option) {
            "1" {
                # Editar estudo
                Write-Host "`nEstudos disponíveis:" -ForegroundColor Cyan
                $studies | ForEach-Object { Write-Host "- $_" }
                $studyId = Read-Host "`nDigite o ID do estudo que deseja editar (exatamente como mostrado acima)"
                
                # Verificar se estudo existe
                try {
                    # Converter para hashtable
                    $response = Invoke-RestMethod -Uri "http://localhost:8000/study/$studyId" -Method Get
                    $currentData = @{}
                    $response.PSObject.Properties | ForEach-Object { 
                        if ($null -eq $_.Value) {
                            $currentData[$_.Name] = ""
                        } else {
                            $currentData[$_.Name] = $_.Value
                        }
                    }
                    
                    Write-Host "`nDados atuais:" -ForegroundColor Cyan
                    $currentData | ConvertTo-Json | Write-Host
                    
                    $confirm = Read-Host "`nConfirma que deseja editar este estudo? (s/n)"
                    if ($confirm -ne "s") { continue }
                    
                    # Lista de campos
                    $fields = @(
                        "Study_ID", "First_Author", "Year", "Country", "Study_Design",
                        "Risk_of_Bias", "Diagnostic_Criteria", "Total_Sample_Size",
                        "Treatment_Group_N", "Control_Group_N", "Age_Mean_SD",
                        "Male_Percentage", "Female_Percentage", "Other_Demographics",
                        "Headache_Percentage", "Focal_Seizures_Percentage",
                        "Other_Symptoms", "Treatment_Type", "Albendazole_Dose",
                        "Treatment_Duration_Days", "Number_of_Cycles",
                        "Cycle_Interval_Days", "Praziquantel_Dose",
                        "Corticosteroid_Type", "Antiepileptic_Drug",
                        "Follow_up_Duration_Months", "Imaging_Schedule",
                        "Complete_Resolution_Percentage", "Partial_Resolution_Percentage",
                        "No_Change_Percentage", "Seizure_Reduction_Percentage",
                        "Elevated_Liver_Enzymes_Percentage", "Other_AE", "Comments"
                    )
                    
                    # Garantir que todos os campos existam no hashtable
                    foreach ($field in $fields) {
                        if (-not $currentData.ContainsKey($field)) {
                            $currentData[$field] = ""
                        }
                    }
                    
                    do {
                        Clear-Host
                        Write-Host "`nEditando: $studyId" -ForegroundColor Cyan
                        Write-Host "Campos disponíveis:" -ForegroundColor Cyan
                        for ($i = 0; $i -lt $fields.Count; $i++) {
                            $field = $fields[$i]
                            $value = $currentData[$field]
                            Write-Host "$($i + 1). $field = $value"
                        }
                        
                        Write-Host "`nOpções:" -ForegroundColor Yellow
                        Write-Host "- Digite o número do campo para editar"
                        Write-Host "- Digite 'q' para voltar ao menu principal"
                        
                        $selection = Read-Host "`nEscolha uma opção"
                        
                        if ($selection -ne 'q') {
                            $fieldIndex = [int]$selection - 1
                            if ($fieldIndex -ge 0 -and $fieldIndex -lt $fields.Count) {
                                $field = $fields[$fieldIndex]
                                $currentValue = $currentData[$field]
                                
                                Write-Host "`nCampo: $field" -ForegroundColor Yellow
                                Write-Host "Valor atual: $currentValue"
                                
                                $newValue = Read-Host "Novo valor (Enter para cancelar)"
                                
                                if ($newValue -ne "") {
                                    $confirm = Read-Host "Confirma alteração? (s/n)"
                                    if ($confirm -eq "s") {
                                        try {
                                            # Atualizar o campo no hashtable
                                            $oldId = $studyId
                                            $currentData[$field] = $newValue
                                            
                                            # Enviar objeto completo atualizado
                                            $jsonBody = $currentData | ConvertTo-Json
                                            $response = Invoke-RestMethod `
                                                -Uri "http://localhost:8000/study/$oldId" `
                                                -Method Put `
                                                -Body $jsonBody `
                                                -ContentType "application/json"
                                            
                                            # Se mudou o Study_ID, atualizar o ID de rastreamento
                                            if ($field -eq "Study_ID") {
                                                $oldId = $studyId
                                                $studyId = $newValue
                                                
                                                # Pequena pausa para garantir que o arquivo foi salvo
                                                Start-Sleep -Seconds 1
                                                
                                                # Tentar verificar se o arquivo existe com o novo ID
                                                $maxRetries = 3
                                                $retryCount = 0
                                                $success = $false
                                                
                                                while ($retryCount -lt $maxRetries -and -not $success) {
                                                    try {
                                                        $verifyData = Invoke-RestMethod -Uri "http://localhost:8000/study/$studyId" -Method Get
                                                        $success = $true
                                                    } catch {
                                                        $retryCount++
                                                        Start-Sleep -Seconds 1
                                                    }
                                                }
                                                
                                                if ($success) {
                                                    Write-Host "`nID atualizado com sucesso!" -ForegroundColor Green
                                                    Write-Host "ID antigo: $oldId" -ForegroundColor Green
                                                    Write-Host "Novo ID: $studyId" -ForegroundColor Green
                                                    Write-Host "Timestamp: $($response.timestamp)" -ForegroundColor Green
                                                    
                                                    # Atualizar dados locais
                                                    $currentData = @{}
                                                    $verifyData.PSObject.Properties | ForEach-Object { 
                                                        if ($null -eq $_.Value) {
                                                            $currentData[$_.Name] = ""
                                                        } else {
                                                            $currentData[$_.Name] = $_.Value
                                                        }
                                                    }
                                                } else {
                                                    Write-Host "`nAVISO: Arquivo salvo mas não pôde ser verificado" -ForegroundColor Yellow
                                                    Write-Host "Por favor, verifique manualmente" -ForegroundColor Yellow
                                                    $currentData["Study_ID"] = $studyId
                                                }
                                            } else {
                                                # Para outros campos, atualizar dados locais
                                                $response = Invoke-RestMethod -Uri "http://localhost:8000/study/$studyId" -Method Get
                                                $currentData = @{}
                                                $response.PSObject.Properties | ForEach-Object { 
                                                    if ($null -eq $_.Value) {
                                                        $currentData[$_.Name] = ""
                                                    } else {
                                                        $currentData[$_.Name] = $_.Value
                                                    }
                                                }
                                                
                                                Write-Host "`nAtualização realizada!" -ForegroundColor Green
                                                Write-Host "Campo: $field" -ForegroundColor Green
                                                Write-Host "Novo valor: $newValue" -ForegroundColor Green
                                                Write-Host "Timestamp: $($response.timestamp)" -ForegroundColor Green
                                            }
                                            
                                        } catch {
                                            Write-Host "`nERRO na atualização: $_" -ForegroundColor Red
                                            if ($field -eq "Study_ID") {
                                                Write-Host "ID antigo: $oldId" -ForegroundColor Yellow
                                                Write-Host "Tentando usar novo ID: $studyId" -ForegroundColor Yellow
                                            }
                                        }
                                        Read-Host "`nPressione Enter para continuar"
                                    }
                                }
                            } else {
                                Write-Host "Número inválido!" -ForegroundColor Red
                                Start-Sleep -Seconds 1
                            }
                        }
                    } while ($selection -ne 'q')
                    
                } catch {
                    Write-Host "`nERRO: Estudo não encontrado ou erro na API" -ForegroundColor Red
                    Read-Host "Pressione Enter para continuar"
                }
            }
            "2" {
                # Verificar estudo
                $studyId = Read-Host "`nDigite o ID do estudo que deseja verificar"
                try {
                    $data = Invoke-RestMethod -Uri "http://localhost:8000/study/$studyId" -Method Get
                    Write-Host "`nDados do estudo:" -ForegroundColor Cyan
                    $data | ConvertTo-Json -Depth 10 | Write-Host
                    Read-Host "`nPressione Enter para continuar"
                } catch {
                    Write-Host "`nERRO: Estudo não encontrado" -ForegroundColor Red
                    Read-Host "Pressione Enter para continuar"
                }
            }
            "3" {
                # Deletar estudo
                $studyId = Read-Host "`nDigite o ID do estudo que deseja deletar"
                
                try {
                    # Primeiro mostrar os dados do estudo
                    $currentData = Invoke-RestMethod -Uri "http://localhost:8000/study/$studyId" -Method Get
                    
                    Write-Host "`nDados do estudo a ser deletado:" -ForegroundColor Red
                    $currentData | ConvertTo-Json | Write-Host
                    
                    Write-Host "`nATENÇÃO!" -ForegroundColor Red
                    Write-Host "Esta operação não pode ser desfeita!" -ForegroundColor Red
                    $confirm1 = Read-Host "Digite o ID do estudo novamente para confirmar a deleção"
                    
                    if ($confirm1 -eq $studyId) {
                        $confirm2 = Read-Host "Tem certeza absoluta que deseja deletar este estudo? (digite 'DELETAR' para confirmar)"
                        
                        if ($confirm2 -eq "DELETAR") {
                            try {
                                $response = Invoke-RestMethod `
                                    -Uri "http://localhost:8000/study/$studyId" `
                                    -Method Delete
                                
                                Write-Host "`nEstudo deletado com sucesso!" -ForegroundColor Green
                                Write-Host "ID: $studyId" -ForegroundColor Green
                                Write-Host "Timestamp: $($response.timestamp)" -ForegroundColor Green
                                
                            } catch {
                                Write-Host "`nERRO ao deletar: $_" -ForegroundColor Red
                            }
                        } else {
                            Write-Host "`nOperação cancelada pelo usuário" -ForegroundColor Yellow
                        }
                    } else {
                        Write-Host "`nIDs não correspondem. Operação cancelada" -ForegroundColor Yellow
                    }
                    
                } catch {
                    Write-Host "`nERRO: Estudo não encontrado ou erro na API" -ForegroundColor Red
                }
                Read-Host "`nPressione Enter para continuar"
            }
            "4" {
                # Adicionar novo estudo
                Write-Host "`n=== ADICIONAR NOVO ESTUDO ===" -ForegroundColor Cyan
                Write-Host "Cole o JSON do estudo abaixo (pressione Enter duas vezes para finalizar):" -ForegroundColor Yellow
                Write-Host "Certifique-se de incluir pelo menos o campo 'Study_ID'" -ForegroundColor Yellow
                
                $lines = @()
                do {
                    $line = Read-Host
                    if ($line -eq "") {
                        break
                    }
                    $lines += $line
                } while ($true)
                
                $jsonContent = $lines -join "`n"
                
                try {
                    # Verificar se é um JSON válido
                    $studyData = $jsonContent | ConvertFrom-Json
                    
                    # Verificar se tem Study_ID
                    if (-not $studyData.Study_ID) {
                        Write-Host "`nERRO: JSON deve conter o campo 'Study_ID'" -ForegroundColor Red
                        Read-Host "Pressione Enter para continuar"
                        continue
                    }
                    
                    # Verificar se já existe
                    try {
                        $existing = Invoke-RestMethod -Uri "http://localhost:8000/study/$($studyData.Study_ID)" -Method Get
                        Write-Host "`nAVISO: Já existe um estudo com este ID!" -ForegroundColor Red
                        Write-Host "Use a opção de editar para modificar estudos existentes." -ForegroundColor Yellow
                        Read-Host "Pressione Enter para continuar"
                        continue
                    } catch {
                        # Se der 404, está ok - podemos criar
                    }
                    
                    # Mostrar dados para confirmação
                    Write-Host "`nDados do novo estudo:" -ForegroundColor Cyan
                    $studyData | ConvertTo-Json -Depth 10 | Write-Host
                    
                    $confirm = Read-Host "`nConfirma a criação deste estudo? (s/n)"
                    if ($confirm -eq "s") {
                        try {
                            # Enviar para API
                            $headers = @{
                                "Content-Type" = "application/json"
                            }
                            
                            $response = Invoke-RestMethod `
                                -Uri "http://localhost:8000/study" `
                                -Method Post `
                                -Headers $headers `
                                -Body ([System.Text.Encoding]::UTF8.GetBytes($jsonContent)) `
                                -ContentType "application/json"
                            
                            Write-Host "`nEstudo criado com sucesso!" -ForegroundColor Green
                            Write-Host "ID: $($studyData.Study_ID)" -ForegroundColor Green
                            Write-Host "Timestamp: $($response.timestamp)" -ForegroundColor Green
                        } catch {
                            Write-Host "`nERRO ao criar estudo:" -ForegroundColor Red
                            Write-Host $_.Exception.Message -ForegroundColor Red
                            if ($_.ErrorDetails.Message) {
                                Write-Host "Detalhes: $($_.ErrorDetails.Message)" -ForegroundColor Red
                            }
                        }
                    } else {
                        Write-Host "`nOperação cancelada pelo usuário" -ForegroundColor Yellow
                    }
                    
                } catch {
                    Write-Host "`nERRO ao processar JSON: $_" -ForegroundColor Red
                    Write-Host "Detalhes do erro:" -ForegroundColor Red
                    $_.Exception | Format-List -Force
                }
                Read-Host "`nPressione Enter para continuar"
            }
            "5" {
                Write-Host "`nSaindo..." -ForegroundColor Yellow
                return
            }
            default {
                Write-Host "`nOpção inválida!" -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    } while ($true)
}

# Executar função interativa
Edit-StudyInteractive 