import migrateReportsDirectoryName from './reports_directory_name';

export function jobMigrationTasksRun(context) {
  context.xcyber360.logger.debug('Migration tasks started');
  const migrationTasks = [migrateReportsDirectoryName];

  migrationTasks.forEach(task => task(context));
}
