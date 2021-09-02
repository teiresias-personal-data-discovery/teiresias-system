import { useEffect, useCallback } from 'react';
import _ from 'lodash';

import Login from '../Base/Login';
import Reports from './Reports';
import Repositories from './Variables/Repositories';
import Storages from './Variables/Storages';
import DataInput from './DataInput';
import useReportUser from '../hooks/useReportUser';
import useVariables from '../hooks/useVariables';
import useReports from '../hooks/useReports';
import useWorkflow from '../hooks/useWorkflow';

const airflowApiKeys = ['env', 'git', 'dataInput'];
const variablesKeys = ['env', 'git'];

const Page = ({ activeKey }) => {
  const {
    tokenReportUser,
    loginReportUser,
    isLoadingReportUser,
    reportUserError,
  } = useReportUser();

  const {
    reports,
    isLoadingData,
    dataError,
    setFilter,
    setToken,
    fetchReports,
  } = useReports();

  const {
    headers,
    repositories,
    storageCredentials,
    isLoadingVariables,
    variablesError,
    airflowUserError,
    setAirflowCredentials,
    fetchVariables,
    postVariables,
    variablesStatus,
  } = useVariables();

  const { triggerWorkflow, workflowStatuses } = useWorkflow();

  const workflowTrigger = useCallback(
    (workflow) => (conf) => {
      triggerWorkflow({ workflow, headers, conf: conf || {} });
    },
    [headers, triggerWorkflow]
  );

  useEffect(() => {
    if (variablesKeys.includes(activeKey) && headers) {
      fetchVariables();
    }
    if (activeKey === 'reporting' && tokenReportUser) {
      fetchReports();
    }
  }, [activeKey, fetchVariables, fetchReports, tokenReportUser, headers]);

  if (airflowApiKeys.includes(activeKey) && (!headers || airflowUserError)) {
    return (
      <Login
        isLoading={isLoadingVariables}
        title="Airflow API"
        login={setAirflowCredentials}
        userError={airflowUserError}
      />
    );
  }

  switch (activeKey) {
    case 'dataInput':
      return (
        <DataInput
          workflowStatus={_.get(workflowStatuses, 'dataInput')}
          triggerWorkflow={workflowTrigger('dataInput')}
        />
      );
    case 'env':
      return (
        <Storages
          workflowStatus={_.get(workflowStatuses, 'storages')}
          triggerWorkflow={workflowTrigger('storages')}
          storageCredentials={storageCredentials}
          isLoading={isLoadingVariables}
          variablesError={variablesError}
          fetchStorageCredentials={fetchVariables}
          postStorageCredentials={postVariables('storages')}
          variablesStatus={variablesStatus}
        />
      );
    case 'git':
      return (
        <Repositories
          workflowStatus={_.get(workflowStatuses, 'repositories')}
          triggerWorkflow={workflowTrigger('repositories')}
          repositories={repositories}
          isLoading={isLoadingVariables}
          variablesError={variablesError}
          fetchRepositories={fetchVariables}
          postRepositories={postVariables('repositories')}
          variablesStatus={variablesStatus}
        />
      );
    default:
      return tokenReportUser ? (
        <Reports
          token={tokenReportUser}
          reports={reports}
          isLoadingData={isLoadingData}
          dataError={dataError}
          setFilter={setFilter}
          setToken={setToken}
          fetchReports={fetchReports}
        />
      ) : (
        <Login
          isLoading={isLoadingReportUser}
          title="Report"
          login={loginReportUser}
          userError={reportUserError}
        />
      );
  }
};

export default Page;
