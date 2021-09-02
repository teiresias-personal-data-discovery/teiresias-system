import _ from 'lodash';
import { evaluation } from '../../Base/constants';

export const summarizeReport = (report, type) => {
  switch (type) {
    case 'json':
      return _.reduce(
        report,
        (acc, facts, reportId) => {
          const meanProximities =
            _.chain(facts)
              .filter({ type: 'key' })
              .uniqBy('candidate')
              .meanBy(({ proximity }) =>
                _.chain(proximity).first().nth(1).value()
              )
              .toInteger()
              .value() / 100;
          const collectionReport = {
            numberOfEntities: 1,
            hasDataMatches: !!_.find(facts, { type: 'value' }),
            meanProximities,
          };
          const collectionMetric = evaluation.metric(collectionReport);
          return {
            ...acc,
            [reportId]: {
              ...collectionReport,
              collectionMetric,
            },
            reportHasPersonalData: collectionMetric > 0,
          };
        },
        {}
      );
    default:
      return _.reduce(
        report,
        (traces, storageReport, storageName) => {
          const collectionEvaluation = _.chain(storageReport)
            .get('meta_data_analysis')
            .omit('storage_type')
            .reduce(
              (storageTraces, collectionMetaReport, collectionName) => {
                const storageType = _.get(collectionMetaReport, 'storage_type');
                const proximities = _.get(
                  collectionMetaReport,
                  storageType === 'mongo'
                    ? 'key_proximities'
                    : 'column_proximities',
                  {}
                );
                let meanProximities = 0;
                if (!_.isEmpty(proximities)) {
                  meanProximities =
                    _.chain(proximities)
                      .values()
                      .meanBy((proximityPair) =>
                        _.nth(_.nth(proximityPair, 0), 1)
                      )
                      .value() / 100;
                }
                const hasDataMatches =
                  _.chain(storageReport)
                    .get(['data_analysis', collectionName], {})
                    .omit(['primary_keys', 'error'])
                    .keys()
                    .value().length > 0;
                const collectionReport = {
                  numberOfEntities: collectionMetaReport.number_of_entities,
                  hasDataMatches,
                  meanProximities,
                };
                const collectionMetric = evaluation.metric(collectionReport);
                return {
                  ...storageTraces,
                  [collectionName]: { ...collectionReport, collectionMetric },
                  storageHasPersonalData:
                    storageTraces.storageHasPersonalData ||
                    collectionMetric > 0,
                };
              },
              { storageHasPersonalData: false }
            )
            .value();
          const {
            storageHasPersonalData,
            ...collectionReports
          } = collectionEvaluation;
          return {
            ...traces,
            [storageName]: collectionReports,
            reportHasPersonalData:
              traces.reportHasPersonalData || storageHasPersonalData,
          };
        },
        { reportHasPersonalData: false }
      );
  }
};
