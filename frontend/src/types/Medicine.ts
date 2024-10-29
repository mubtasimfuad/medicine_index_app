// frontend/src/types/Medicine.ts
export interface Medicine {
    id: number;
    name: string;
    generic_name: string;
    manufacturer: string;
    description?: string; // Optional fields if any
    price?: number;
    batch_number?: string;
  }
  