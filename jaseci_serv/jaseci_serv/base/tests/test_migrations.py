from django_test_migrations.contrib.unittest_case import MigratorTestCase

class TestDirectMigrations(MigratorTestCase):
    """Test direct migrations for the base app"""
    migrate_from = ('base', '0002_jaseci_1_to_1_3')
    migrate_to = ('base', '0003_swap_kind_and_name')

    def prepare(self):
        """Data preparation"""
        jaseci_object = self.old_state.apps.get_model('base', 'JaseciObject')
        jaseci_object.objects.create(
            name='object_name',
            kind='object_kind'
        )

    def test_migration_base0003(self):
        """Test migration 00003 which swaps the name and kind field"""
        jaseci_object = self.new_state.apps.get_model('base', 'JaseciObject')
        assert jaseci_object.objects.count() == 1
        assert jaseci_object.objects.filter(name='object_name').count() == 0
        assert jaseci_object.objects.filter(kind='object_kind').count() == 0
        new_obj = jaseci_object.objects.get(name='object_kind')
        assert new_obj.kind == 'object_name'


