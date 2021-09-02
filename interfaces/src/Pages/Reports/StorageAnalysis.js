import _ from 'lodash';
import styled from 'styled-components';
import { Collapse } from 'antd';

import { colors } from '../../Base/constants';
import {
  MetaDataFindingListItem,
  DataFindingListItem,
} from './DataAnalysisItem.js';
import CollectionHeader from './CollectionHeader';

export const Highlight = styled.span`
  font-style: italic;
  padding-left: 0.3em;
  padding-right: 0.3em;
`;

export const StorageName = styled.span`
  color: ${colors.tertiary};
  font-size: 20px;
  font-style: italic;
  padding-bottom: 5px;
  line-height: 1em;
  width: 200px;
`;

export const MetaDetail = styled.ul`
  color: ${colors.tertiary};
`;

const StorageType = styled.span`
  margin: 0 20px;
`;

const labels = {
  mongo: 'MongoDB',
  postgre: 'PostgreSQL',
};

const StorageDataAnalysis = ({ report, summary }) => (
  <ul>
    {_.map(report, (storageReport, storageName) => {
      const storageType = _.get(storageReport, [
        'meta_data_analysis',
        'storage_type',
      ]);
      return (
        <li key={storageName}>
          <StorageName>{storageName}</StorageName>
          <StorageType>{_.get(labels, storageType)}</StorageType>
          {storageReport.meta_data_analysis && (
            <ul>
              {_.map(
                storageReport.meta_data_analysis,
                (collectionReport, collectionName) => {
                  const collectionSummary = _.get(summary, [
                    storageName,
                    collectionName,
                  ]);
                  return (
                    collectionName !== 'storage_type' && (
                      <li key={collectionName}>
                        <CollectionHeader
                          collectionName={collectionName}
                          collectionSummary={collectionSummary}
                        />
                        <Collapse ghost>
                          <Collapse.Panel
                            header="Meta-Data Analysis Details:"
                            key="1"
                          >
                            <MetaDetail>
                              {_.map(
                                collectionReport,
                                (value, category) =>
                                  category !== 'number_of_entities' && (
                                    <MetaDataFindingListItem
                                      key={category}
                                      category={category}
                                      value={value}
                                      storageType={storageType}
                                    />
                                  )
                              )}
                            </MetaDetail>
                          </Collapse.Panel>
                          <Collapse.Panel
                            header="Data Analysis Details:"
                            key="2"
                          >
                            <MetaDetail>
                              {_.map(
                                _.get(
                                  storageReport,
                                  ['data_analysis', collectionName],
                                  {}
                                ),
                                (value, category) => (
                                  <DataFindingListItem
                                    key={category}
                                    category={category}
                                    value={value}
                                    storageType={storageType}
                                  />
                                )
                              )}
                            </MetaDetail>
                          </Collapse.Panel>
                        </Collapse>
                      </li>
                    )
                  );
                }
              )}
            </ul>
          )}
        </li>
      );
    })}
  </ul>
);

export default StorageDataAnalysis;
