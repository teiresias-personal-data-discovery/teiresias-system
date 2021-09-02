import { useMemo } from 'react';
import _ from 'lodash';
import styled from 'styled-components';
import { Collapse } from 'antd';

import CollectionHeader from './CollectionHeader';
import { MetaDetail } from './StorageAnalysis';

export const Highlight = styled.span`
  font-style: italic;
  padding-left: 0.3em;
  padding-right: 0.3em;
`;

const LIMIT = 10;

const JsonDataAnalysis = ({ report, summary }) => {
  const jsonIdentifier = useMemo(() => _.chain(report).keys().first().value(), [
    report,
  ]);

  const uniqueCandidates = useMemo(
    () => _.chain(report).get(jsonIdentifier).uniqBy('candidate').value(),
    [report, jsonIdentifier]
  );

  const keyMatches = useMemo(
    () =>
      _.chain(uniqueCandidates)
        .filter({ type: 'key' })
        .orderBy(
          (item) => _.chain(item).get('proximity').first().last().value(),
          'desc'
        )
        .value(),
    [uniqueCandidates]
  );

  const dataMatches = useMemo(
    () => _.chain(uniqueCandidates).filter({ type: 'value' }).value(),
    [uniqueCandidates]
  );

  return (
    <ul>
      <li>
        <CollectionHeader
          collectionName={jsonIdentifier}
          collectionSummary={_.get(summary, jsonIdentifier)}
          isJSONReport
        />

        <Collapse ghost>
          <Collapse.Panel header="Meta-Data Analysis Details:" key="1">
            <MetaDetail>
              <ul>
                {_.chain(keyMatches)
                  .take(LIMIT)
                  .map(({ candidate, proximity }) => (
                    <li key={candidate}>
                      {candidate} of type key has proximities
                      {proximity.map(
                        (item) => ` ${_.first(item)} ${_.last(item)}% `
                      )}
                    </li>
                  ))
                  .value()}
                {keyMatches.length > LIMIT && (
                  <li>... (Results are limited to {LIMIT} items.)</li>
                )}
              </ul>
            </MetaDetail>
          </Collapse.Panel>
          <Collapse.Panel header="Data Analysis Details:" key="2">
            <MetaDetail>
              <ul>
                {_.chain(dataMatches)
                  .take(LIMIT)
                  .map(({ candidate, pattern }) => (
                    <li
                      key={candidate}
                    >{`${candidate} of type value matched ${pattern}`}</li>
                  ))
                  .value()}
                {dataMatches.length > LIMIT && (
                  <li>... (Results are limited to {LIMIT} items.)</li>
                )}
              </ul>
            </MetaDetail>
          </Collapse.Panel>
        </Collapse>
      </li>
    </ul>
  );
};

export default JsonDataAnalysis;
