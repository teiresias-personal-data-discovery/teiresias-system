import { useMemo, useState } from 'react';
import _ from 'lodash';
import { Tabs } from 'antd';

import Card from '../../Base/Card';
import Flex from '../../Base/Flex';

import DataAnalysis from './DataAnalysis';
import CodeAnalysis from './CodeAnalysis';
import ReportHeader from './ReportHeader';

const { TabPane } = Tabs;

const Report = ({ report }) => {
  const [hasPersonalDataMatch, setHasPersonalDataMatch] = useState(false);

  const numberOfRepoCodeAnalysis = useMemo(
    () =>
      _.chain(report).get('repository_code_analyzer', {}).keys().value().length,
    [report]
  );
  const numberOfStorageDataAnalysis = useMemo(
    () =>
      _.chain(report).get('storage_data_analyzer', {}).keys().value().length,
    [report]
  );
  const hasManuallyCodeAnalysis = useMemo(
    () => _.has(report, 'manually_code_analyzer'),
    [report]
  );
  const hasJSONDataAnalysis = useMemo(
    () => _.has(report, 'json_data_analyzer'),
    [report]
  );

  const defaultKey = useMemo(() => {
    if (numberOfStorageDataAnalysis > 0 || hasJSONDataAnalysis) {
      return 'data_analyzer';
    }
    if (numberOfRepoCodeAnalysis > 0 || hasManuallyCodeAnalysis) {
      return 'code_analyzer';
    }
  }, [
    numberOfStorageDataAnalysis,
    numberOfRepoCodeAnalysis,
    hasJSONDataAnalysis,
    hasManuallyCodeAnalysis,
  ]);

  return (
    <Card
      width="700px"
      title={
        <ReportHeader
          date={report.date}
          numberOfRepoCodeAnalysis={numberOfRepoCodeAnalysis}
          hasManuallyCodeAnalysis={hasManuallyCodeAnalysis}
          numberOfStorageDataAnalysis={numberOfStorageDataAnalysis}
          hasJSONDataAnalysis={hasJSONDataAnalysis}
          hasPersonalDataMatch={hasPersonalDataMatch}
        />
      }
    >
      <Tabs defaultActiveKey={defaultKey}>
        {(numberOfStorageDataAnalysis > 0 || hasJSONDataAnalysis) && (
          <TabPane tab="Data Analysis" key="data_analyzer">
            <DataAnalysis
              type={hasJSONDataAnalysis ? 'json' : 'storage'}
              report={report.storage_data_analyzer || report.json_data_analyzer}
              setHasPersonalDataMatch={setHasPersonalDataMatch}
            />
          </TabPane>
        )}
        {(numberOfRepoCodeAnalysis > 0 || hasManuallyCodeAnalysis) && (
          <TabPane tab="Code Analysis" key="code_analyzer">
            <CodeAnalysis
              report={
                report.repository_code_analyzer || report.manually_code_analyzer
              }
            />
          </TabPane>
        )}
      </Tabs>
      <Flex>Workflow ID: {report.dag_run}</Flex>
    </Card>
  );
};

export default Report;
