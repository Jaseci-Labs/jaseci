from django_test_migrations.contrib.unittest_case import MigratorTestCase

import uuid


class TestMigrationsBase0002(MigratorTestCase):
    """Test direct migrations for the base app"""
    migrate_from = ('base', '0001_initial')
    migrate_to = ('base', '0002_jaseci_1_to_1_3')
    old_user = ''
    old_jaseci_obj = ''

    def prepare(self):
        """Data preparation"""
        jaseci_object = self.old_state.apps.get_model('base', 'JaseciObject')
        users = self.old_state.apps.get_model('base', 'User')
        self.old_user = users.objects.create(
            email='test@test.test',
            name='djano-migration-tester'
        )
        self.old_jaseci_obj = jaseci_object.objects.create(
            user=self.old_user,
            j_owner=uuid.uuid4(),
            name='test_obj'
        )

    def test_migration_base0002(self):
        """
        Test migration 00002 which upgrade jaseci from 1 to 1.2
        j_owner --> j_parent
        user.master --> j_master
        """
        jaseci_object = self.new_state.apps.get_model('base', 'JaseciObject')
        new_obj = jaseci_object.objects.get(name='test_obj')
        assert new_obj.j_parent == self.old_jaseci_obj.j_owner
        assert new_obj.j_master == self.old_user.master


class TestMigrationsBase0003(MigratorTestCase):
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