import _ from 'lodash';
import { Collapse } from 'antd';
import styled from 'styled-components';

import { colors } from '../../Base/constants';

export const Highlight = styled.span`
  font-style: italic;
  padding-left: 0.3em;
  padding-right: 0.3em;
`;

const Error = styled.span`
  color: ${colors.error};
`;

const ErrorPanel = styled(Collapse.Panel)`
  .ant-collapse-header {
    padding-bottom: 0 !important;
  }
`;

const labels = {
  personal_data_typed_columns: 'columns with personal data related types',
  str_columns: 'columns of type text',
  key_names: 'key names',
  column_proximities: 'proximities of column to identifier',
  key_proximities: 'proximities of keys to identifier',
  primary_keys: 'primary keys',
};

export const CollapsedError = ({ error }) => {
  let message = typeof error === 'string' && error;
  if (!message) {
    try {
      message = error.message || JSON.stringify(error);
    } catch {
      message = 'unknown error';
    }
  }
  return (
    <Collapse ghost>
      <ErrorPanel header={<Error>Error:</Error>} key="1">
        <p>{message}</p>
      </ErrorPanel>
    </Collapse>
  );
};

export const MetaDataFindingListItem = ({ category, value, storageType }) => {
  const categoryName = storageType === 'mongo' ? 'key' : 'column';
  switch (category) {
    case 'column_proximities':
    case 'key_proximities':
      return (
        <li>
          {_.get(labels, category)}:
          <ul>
            {_.map(value, (proximityList, columnName) => (
              <li key={columnName}>
                {categoryName}
                <Highlight>{columnName}</Highlight>has proximities
                {proximityList.map((proximityPair) => (
                  <Highlight>
                    {proximityPair[0]} {proximityPair[1]}%
                  </Highlight>
                ))}
              </li>
            ))}
          </ul>
        </li>
      );
    case 'personal_data_typed_columns':
      return (
        <li>
          {_.get(labels, category)}:
          <ul>
            {_.map(value, (meaningList, columnName) => (
              <li key={columnName}>
                {categoryName}
                <Highlight>{columnName}</Highlight>has types
                <Highlight>{meaningList?.join(', ')}</Highlight>
              </li>
            ))}
          </ul>
        </li>
      );
    case 'str_columns':
    case 'key_names':
      return (
        <li>
          {_.get(labels, category)}:<Highlight>{value?.join(', ')}</Highlight>
        </li>
      );
    default:
      return (
        <li>
          {_.get(labels, category, category)}:
          <Highlight>{JSON.stringify(value)}</Highlight>
        </li>
      );
  }
};

export const DataFindingListItem = ({ storageType, category, value }) => {
  const categoryName = storageType === 'mongo' ? 'key' : 'column';
  switch (category) {
    case 'error':
      return (
        <li>
          <CollapsedError error={value} />
        </li>
      );
    case 'primary_keys':
      return (
        <li>
          {_.get(labels, category, category)}:
          <Highlight>{value?.join(', ')}</Highlight>
        </li>
      );
    default:
      return (
        <li>
          {categoryName}
          <Highlight>{category}</Highlight>:
          <ul>
            {_.map(value, (patternReport, patternName) => {
              if (patternName === 'error') {
                return (
                  <li key={patternName}>
                    <CollapsedError error={patternReport} />
                  </li>
                );
              }
              const hasPKList = _.has(patternReport, 'pk_references');
              const hasReferenceList = _.has(patternReport, 'references');
              return (
                <li key={patternName}>
                  <Highlight>{patternName}</Highlight> matched on entities:
                  <Highlight>
                    {hasReferenceList &&
                      _.get(patternReport, 'references', []).join(', ')}
                    {hasPKList &&
                      _.chain(patternReport)
                        .get('pk_references')
                        .reduce(
                          (joinedList, pk_referenceList) =>
                            `${joinedList}, (${pk_referenceList?.join(', ')})`,
                          ''
                        )
                        .value()}
                  </Highlight>
                </li>
              );
            })}
          </ul>
        </li>
      );
  }
};
