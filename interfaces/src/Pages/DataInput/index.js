import { useState, useCallback, useEffect } from 'react';
import { Button, Input, notification } from 'antd';
import { CloudUploadOutlined } from '@ant-design/icons';
import JSONInput from 'react-json-editor-ajrm/index';
import locale from 'react-json-editor-ajrm/locale/en';
import styled from 'styled-components';
import _ from 'lodash';

import Buttons from '../Buttons';
import { Wrapper } from '../Variables/Repositories';

const inputStyle = {
  container: {
    width: '100%',
  },
  body: {
    fontSize: '14px',
    width: undefined,
    display: 'flex',
  },
  outerBox: {
    width: '100%',
  },
  contentBox: {
    width: undefined,
    flex: 1,
  },
  warningBox: {
    width: '100%',
  },
};

const Identifier = styled(Input)`
  height: 40px;
  margin-right: 5px;
`;

const placeholder = { Teiresias: 'Paste your analyzable JSON here.' };

const DataInput = ({
  workflowStatus,
  triggerWorkflow,
  headers,
  resetWorkflowStatus,
}) => {
  const [analysisTitle, setAnalysisTitle] = useState(null);
  const [json, setJson] = useState(placeholder);

  const handleJsonInput = useCallback((input) => {
    if (!input.error) {
      setJson(input.json);
    }
  }, []);

  const triggerDataAnalysis = useCallback(() => {
    triggerWorkflow({
      workflow: 'dataInput',
      headers,
      conf: { dataIdentifier: analysisTitle, data: json },
    });
  }, [triggerWorkflow, headers, analysisTitle, json]);

  const setTitle = useCallback((event) => {
    setAnalysisTitle(event.target.value);
  }, []);

  const openNotification = useCallback((status) => {
    if (status === 'success') {
      notification.success({
        message: `Successfully started Analysis`,
        description: '',
      });
    }
    if (status === 'error') {
      notification.info({
        message: `Something went wrong`,
        description: '',
      });
    }
  }, []);

  const resetInputs = useCallback(() => {
    setTimeout(() => {
      setAnalysisTitle(null);
      setJson(null);
    }, 2000);
  }, [setAnalysisTitle, setJson]);

  useEffect(() => {
    if (workflowStatus === 'success') {
      openNotification('success');
      resetWorkflowStatus();
      resetInputs();
    }
    if (workflowStatus === 'error') {
      openNotification('error');
      resetWorkflowStatus();
    }
  }, [workflowStatus, openNotification, resetInputs, resetWorkflowStatus]);

  return (
    <Wrapper column align="center">
      <Buttons error={workflowStatus === 'error' && workflowStatus}>
        <Identifier
          size="small"
          placeholder="input JSON identifier"
          onChange={setTitle}
        />

        <Button
          type="primary"
          size="large"
          icon={<CloudUploadOutlined />}
          onClick={triggerDataAnalysis}
          disabled={
            _.isEmpty(json) ||
            !analysisTitle ||
            (workflowStatus === 'pending' && !headers)
          }
        >
          Analyze JSON
        </Button>
      </Buttons>
      <JSONInput
        style={inputStyle}
        onChange={handleJsonInput}
        placeholder={placeholder}
        theme="light_mitsuketa_tribute"
        locale={locale}
        height="80vh"
      />
    </Wrapper>
  );
};
export default DataInput;
