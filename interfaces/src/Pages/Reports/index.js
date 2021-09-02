import { useEffect } from 'react';
import { Empty } from 'antd';
import _ from 'lodash';
import styled from 'styled-components';

import Report from './Report';
import Buttons from '../Buttons';
import ErrorBoundary from '../../Base/ErrorBoundary';
import { Wrapper } from '../Variables/Repositories';

const NoData = styled(Empty)`
  .ant-empty-description {
    color: white;
  }
`;
const RenderData = ({ reports }) => {
  if (_.isEmpty(reports)) {
    return (
      <NoData image={Empty.PRESENTED_IMAGE_SIMPLE} description="No Reports" />
    );
  }
  return reports.map((report) => (
    <ErrorBoundary domain="report" key={report._id}>
      <Report report={report} />
    </ErrorBoundary>
  ));
};

const Reports = ({
  token,
  reports,
  isLoadingData,
  dataError,
  setToken,
  fetchReports,
}) => {
  useEffect(() => {
    if (token) {
      setToken(token);
    }
  }, [token, setToken]);

  return (
    <Wrapper column align="center">
      <Buttons
        isLoading={isLoadingData}
        error={dataError}
        fetch={fetchReports}
      />
      {reports && <RenderData reports={reports} />}
    </Wrapper>
  );
};

export default Reports;
