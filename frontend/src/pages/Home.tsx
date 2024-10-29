// HomePage.tsx
import React, { useState } from "react";
import MedicineListComponent from "../components/Search/MedicineListComponent";
import FilteredMedicineListComponent from "../components/Search/FilteredMedicineListComponent";
import SearchBarComponent from "../components/Search/SearchBarComponent";

const HomePage: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [filters, setFilters] = useState<any>({});
  const [isSearching, setIsSearching] = useState<boolean>(false);

  const handleSearch = (query: string, filters: any) => {
    setQuery(query);
    setFilters(filters);
    setIsSearching(true);
  };

  return (
    <div>
      <SearchBarComponent onSearch={handleSearch} />
      {isSearching ? (
        <FilteredMedicineListComponent query={query} filters={filters} />
      ) : (
        <MedicineListComponent />
      )}
    </div>
  );
};

export default HomePage;
