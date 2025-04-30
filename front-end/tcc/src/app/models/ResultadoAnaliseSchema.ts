import { DadoAnalise } from "./DadoAnalise"

export interface ResultadoAnaliseSchema {
  total_medicoes: number
  anomalias: number
  mensagem: string
  dados: DadoAnalise[]
  ultimo_valor: number
  maximo: number
  minimo: number
  data_inicio: string
  data_fim: string,
  dados_insuficientes: boolean
}
