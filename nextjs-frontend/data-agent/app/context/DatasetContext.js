'use client';
import React, { createContext, useState, useContext } from 'react';

const DatasetContext = createContext();

export const DatasetProvider = ({ children }) => {
  const [datasetPath, setDatasetPath] = useState('');
  return (
    <DatasetContext.Provider value={{ datasetPath, setDatasetPath }}>
      {children}
    </DatasetContext.Provider>
  );
};

export const useDataset = () => useContext(DatasetContext);
