'use client';

import React from 'react';
import MainContent from '../app/components/mainContent';

export default function Home({ datasetPath, setDatasetPath }) {
  return (
    <MainContent datasetPath={datasetPath} setDatasetPath={setDatasetPath} />
  );
}
