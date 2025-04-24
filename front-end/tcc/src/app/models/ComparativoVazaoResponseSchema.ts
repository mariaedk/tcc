import { SerieComparativaSchema } from "./SerieComparativaSchema";

export interface ComparativoVazaoResponseSchema {
  categorias: string[],
  series: SerieComparativaSchema[]
}
