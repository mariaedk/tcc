import { TipoMedicao } from "./TipoMedicao";

export interface FiltroData {
  tipoMedicao: TipoMedicao;
  data?: Date;
  dataInicio?: Date;
  dataFim?: Date;
}
