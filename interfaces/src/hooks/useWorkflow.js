import { useState, useCallback } from 'react';
import _ from 'lodash';
import { checkResponseStatus } from './useVariables';

const dagMap = {
  dataInput: { id: 'X_triggered_data_analysis', timeout: 0 },
  repositories: { id: 'A1_repository_code_analysis', timeout: 10 },
  storages: { id: 'B_storage_data_analysis', timeout: 10 },
};

const bodyGenerator = ({ workflowId, conf }) => ({
  conf: conf || {},
  dag_run_id: workflowId,
  execution_date: new Date().toISOString(),
});

const workflowEndpoint = (workflow) =>
  `${
    process.env.REACT_APP_AIRFLOW_BASE || 'https://airflow.docker.localhost'
  }/api/v1/dags/${_.get(dagMap, [workflow, 'id'])}/dagRuns`;

const useWorkflow = () => {
  const [workflowStatuses, setWorkflowStatuses] = useState({
    dataInput: null,
    repository: null,
    storage: null,
  });

  const triggerWorkflow = useCallback(
    ({ workflow, headers, conf }) => {
      if (headers) {
        setWorkflowStatuses((prevWorkflowStatuses) => ({
          ...prevWorkflowStatuses,
          [workflowEndpoint]: 'pending',
        }));
        try {
          fetch(workflowEndpoint(workflow), {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(bodyGenerator({ workflow, conf })),
          })
            .then((response) => {
              checkResponseStatus(response.Status);
              setWorkflowStatuses((prevWorkflowStatuses) => ({
                ...prevWorkflowStatuses,
                [workflow]: 'success',
              }));
            })
            .catch(() => {
              setWorkflowStatuses((prevWorkflowStatuses) => ({
                ...prevWorkflowStatuses,
                [workflow]: 'error',
              }));
            });
        } catch {
          setWorkflowStatuses((prevWorkflowStatuses) => ({
            ...prevWorkflowStatuses,
            [workflow]: 'error',
          }));
        }
      }
    },
    [setWorkflowStatuses]
  );

  return {
    triggerWorkflow,
    workflowStatuses,
  };
};
export default useWorkflow;
