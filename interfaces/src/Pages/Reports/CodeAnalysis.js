import _ from 'lodash';
import { Collapse } from 'antd';

import { Highlight } from './DataAnalysis';

const CodeAnalysis = ({ report }) => (
  <ul>
    {_.map(report, (repositoryReport, repository) => {
      if (repositoryReport.error) {
        return (
          <li>
            repository <Highlight>{repository}</Highlight>
            <ul>
              <li>error: {repositoryReport.error}</li>
            </ul>
          </li>
        );
      }
      const {
        number_of_storages_found,
        number_of_total_missing_values,
        analyzed_files,
        missing_values,
      } = repositoryReport;
      return (
        <li>
          repository <Highlight>{repository}</Highlight>
          <ul>
            <li>
              storages found:
              <Highlight>{number_of_storages_found}</Highlight>
              {number_of_total_missing_values && (
                <>
                  {'// total missing values:'}
                  <Highlight>{number_of_total_missing_values}</Highlight>
                </>
              )}
            </li>
            <li>
              missing values:
              <Highlight>
                <ul>
                  {_.map(missing_values, ({ values }, storageName) => (
                    <li>
                      storage {storageName}:
                      <Highlight>{values?.join(', ')}</Highlight>
                    </li>
                  ))}
                </ul>
              </Highlight>
            </li>
            <li>
              <Collapse ghost>
                <Collapse.Panel header="analyzed files:" key="1">
                  <Highlight>{analyzed_files?.join(', ')}</Highlight>
                </Collapse.Panel>
              </Collapse>
            </li>
          </ul>
        </li>
      );
    })}
  </ul>
);
export default CodeAnalysis;
