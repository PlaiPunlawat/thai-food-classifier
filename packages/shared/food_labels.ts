import data from "./food_labels.json";

export interface FoodLabel {
  id: number;
  name_th: string;
  name_en: string;
  name_en_alt: string[];
}

export const FOOD_LABELS: FoodLabel[] = data.labels as FoodLabel[];
