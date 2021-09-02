import { useMemo, useEffect } from 'react';
import styled from 'styled-components';

import { summarizeReport } from './utils';
import StorageDataAnalysis from './StorageAnalysis';
import JsonDataAnalysis from './JSONAnalysis';

export const Highlight = styled.span`
  font-style: italic;
  padding-left: 0.3em;
  padding-right: 0.3em;
`;

const DataAnalysis = ({ report, type, setHasPersonalDataMatch }) => {
  const summary = useMemo(() => summarizeReport(report, type), [report, type]);

  useEffect(() => {
    if (summary.reportHasPersonalData) {
      setHasPersonalDataMatch(true);
    }
  }, [summary, setHasPersonalDataMatch]);

  switch (type) {
    case 'json':
      return <JsonDataAnalysis report={report} summary={summary} />;
    default:
      return <StorageDataAnalysis report={report} summary={summary} />;
  }
};

export default DataAnalysis;
