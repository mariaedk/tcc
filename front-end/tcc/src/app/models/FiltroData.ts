import { TipoConsulta } from "./TipoConsulta";

export interface FiltroData {
  tipoConsulta: TipoConsulta;
  data?: Date;
  dataInicio?: Date;
  dataFim?: Date;
}
