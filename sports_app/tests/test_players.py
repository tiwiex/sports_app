from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch
import frappe
from sports_app import players, players_api


class TestPlayers(TestCase):
 def setUp(self):
  def throw(message, exc=frappe.ValidationError): raise exc(message)
  for target, name, value in ((frappe, 'throw', throw), (frappe, '_', lambda s:s), (players, '_', lambda s:s), (players_api, '_', lambda s:s)):
   active=patch.object(target,name,value);active.start();self.addCleanup(active.stop)

 def fixture(self, **changes):
  doc=frappe._dict(company='Academy', program='Football', group='Under12', payer_customer='Family', start_date='2026-11-01',end_date=None,status='Active')
  doc.update(changes);doc.get_doc_before_save=lambda:None
  return doc

 def validate(self, doc, **changes):
  program=frappe._dict(company='Academy',enabled=1)
  group=frappe._dict(company='Academy',program='Football',enabled=1)
  customer=frappe._dict(disabled=0)
  for key,value in changes.items(): locals()[key].update(value)
  players.validate_enrollment_values(doc,program,group,customer)

 def test_enrollment_dates_and_status(self):
  for changes in ({'end_date':'2026-10-31'},{'status':'Withdrawn'},{'status':'Completed'},{'status':'Other'},{'start_date':None}):
   with self.subTest(changes=changes), self.assertRaises(frappe.ValidationError): self.validate(self.fixture(**changes))
  self.validate(self.fixture(status='Withdrawn',end_date='2026-11-10'))

 def test_cross_company_and_group_and_disabled_payer_rejected(self):
  for changes in ({'program':{'company':'Other'}},{'group':{'program':'Swimming'}},{'group':{'company':'Other'}},{'program':{'enabled':0}},{'group':{'enabled':0}},{'customer':{'disabled':1}}):
   with self.subTest(changes=changes), self.assertRaises(frappe.ValidationError): self.validate(self.fixture(),**changes)

 def test_retired_program_does_not_trap_existing_enrollment(self):
  doc=self.fixture(status='Withdrawn',end_date='2026-11-10');doc.get_doc_before_save=lambda:frappe._dict(program='Football',group='Under12',payer_customer='Family')
  self.validate(doc,program={'enabled':0},group={'enabled':0},customer={'disabled':1})

 def test_eligibility_boundaries_and_suspension(self):
  row=self.fixture(end_date='2026-11-30')
  for day, expected in [('2026-10-31',False),('2026-11-01',True),('2026-11-30',True),('2026-12-01',False)]:
   self.assertEqual(players.is_eligible(row,day),expected)
  for status in ('Pending','Suspended','Withdrawn','Completed'):
   row.status=status;self.assertFalse(players.is_eligible(row,'2026-11-05'))

 def test_finance_and_basic_sports_roles_cannot_manage_players(self):
  fake=SimpleNamespace(session=SimpleNamespace(user='operator'),get_roles=Mock())
  with patch.object(players,'frappe',fake):
   for roles,expected in [(['Accounts Manager'],False),(['Sports Console'],False),(['Sports Registrar'],True),(['Sports Academy Administrator'],True),(['System Manager'],True)]:
    fake.get_roles.return_value=roles;self.assertEqual(players.can_manage_players(),expected)
   self.assertFalse(players.can_manage_players('Guest'))

 def test_player_and_request_provenance_immutable(self):
  doc=self.fixture();doc.get_doc_before_save=lambda:frappe._dict(company='Other')
  with patch.object(players,'validate_company') as company, self.assertRaises(frappe.ValidationError):players.immutable(doc,('company',))
  company.assert_called_once_with('Other')

 def test_arbitrary_write_fields_and_bad_retry_keys_rejected(self):
  with self.assertRaises(frappe.ValidationError): players_api._payload({'owner':'Administrator'},players.PLAYER_FIELDS)
  with patch.object(players_api,'require_player_access'), self.assertRaises(frappe.ValidationError):
   players_api.register_player.__wrapped__({'full_name':'Name'}, {}, 'not-a-uuid')

 def test_all_private_endpoints_require_role(self):
  with patch.object(players_api,'require_player_access',side_effect=frappe.PermissionError):
   for func,args in [(players_api.get_registration_defaults,()),(players_api.list_players,()),(players_api.get_player,('x',)),(players_api.register_player,({},{},'x')),(players_api.save_player,('x',{},'')),(players_api.save_enrollment,('x',{}))]:
    with self.subTest(method=func.__name__), self.assertRaises(frappe.PermissionError):func.__wrapped__(*args)

 def test_customer_selection_not_accepted_from_registration_client(self):
  with self.assertRaises(frappe.ValidationError):
   players_api._payload({'payer_customer':'Family'},players.ENROLLMENT_FIELDS)
  with self.assertRaises(frappe.ValidationError):
   players_api._payload({'customer':'Existing account'},players.PLAYER_FIELDS)

 def test_native_player_cannot_reuse_existing_customer(self):
  from sports_app.sports_app.doctype.sports_player import sports_player
  with patch.object(sports_player,'require_player_access'), self.assertRaises(frappe.ValidationError):
   sports_player.SportsPlayer.before_insert(frappe._dict(customer='Another player customer'))

 def test_native_enrollment_cannot_use_another_player_customer(self):
  from sports_app.sports_app.doctype.sports_enrollment import sports_enrollment
  player=SimpleNamespace(customer='Own Customer',company='Academy',check_permission=Mock())
  doc=SimpleNamespace(player='Player',payer_customer='Other Customer',company='Academy')
  with patch.object(sports_enrollment,'require_player_access'), patch.object(sports_enrollment,'immutable'), patch.object(sports_enrollment.frappe,'get_doc',return_value=player), self.assertRaises(frappe.ValidationError):
   sports_enrollment.SportsEnrollment.validate(doc)

 def test_auto_customer_creation_requires_player_role(self):
  with patch.object(players,'require_player_access',side_effect=frappe.PermissionError), self.assertRaises(frappe.PermissionError):
   players.create_player_customer(SimpleNamespace(company='Academy'))

 def test_parent_customer_group_cannot_be_reused_as_program_category(self):
  program=SimpleNamespace(program_name='Football',company='Academy',enabled=1,check_permission=Mock())
  fake=SimpleNamespace(get_value=Mock(return_value=frappe._dict(name='Football',is_group=1)))
  with patch.object(players,'require_player_access'),patch.object(players,'validate_company'),patch.object(players.frappe,'get_doc',return_value=program),patch.object(players.frappe,'db',fake),self.assertRaises(frappe.ValidationError):
   players.ensure_program_customer_group(SimpleNamespace(registration_program='Program',company='Academy'))

 def test_program_category_requires_matching_company(self):
  program=SimpleNamespace(program_name='Football',company='Other',enabled=1,check_permission=Mock())
  with patch.object(players,'require_player_access'),patch.object(players,'validate_company'),patch.object(players.frappe,'get_doc',return_value=program),self.assertRaises(frappe.ValidationError):
   players.ensure_program_customer_group(SimpleNamespace(registration_program='Program',company='Academy'))


 def test_new_player_requires_unique_email_and_normalizes_it(self):
  for email in ('', None, 'not-an-email'):
   with self.subTest(email=email),self.assertRaises(frappe.ValidationError):players.validate_player_email(frappe._dict(contact_email=email))
  doc=frappe._dict(contact_email=' Player@Example.invalid ')
  with patch.object(players.frappe,'db',SimpleNamespace(exists=Mock(return_value=False))):players.validate_player_email(doc)
  self.assertEqual(doc.contact_email,'player@example.invalid')
  with patch.object(players.frappe,'db',SimpleNamespace(exists=Mock(return_value=True))),self.assertRaises(frappe.ValidationError):players.validate_player_email(doc)

 def test_player_user_is_background_owned_and_not_client_assignable(self):
  with self.assertRaises(frappe.ValidationError):players_api._payload({'portal_user':'Administrator'},players.PLAYER_FIELDS)
  from sports_app.sports_app.doctype.sports_player import sports_player
  with patch.object(sports_player,'require_player_access'),self.assertRaises(frappe.ValidationError):
   sports_player.SportsPlayer.before_insert(frappe._dict(portal_user='Administrator'))

 def test_user_provisioning_requires_player_role(self):
  with patch.object(players,'require_player_access',side_effect=frappe.PermissionError),self.assertRaises(frappe.PermissionError):players.create_player_user(frappe._dict())


 def test_failed_registration_discards_only_its_own_after_commit_callbacks(self):
  from frappe.utils import CallbackManager
  from uuid import uuid4
  original=CallbackManager();earlier=Mock();orphan=Mock();original.add(earlier)
  db=SimpleNamespace(after_commit=original,get_value=Mock(return_value=None),savepoint=Mock(),rollback=Mock())
  def insert_player():
   db.after_commit.add(orphan)
   return SimpleNamespace(name='PLAYER-1',customer='CUSTOMER-1')
  player=SimpleNamespace(insert=insert_player)
  enrollment=SimpleNamespace(insert=Mock(side_effect=frappe.ValidationError('Invalid enrollment')))
  settings=frappe._dict(company='Academy',default_program='Program',default_group=None,default_enrollment_status='Pending')
  with patch.object(players_api,'require_player_access'),patch.object(players_api,'registration_settings',return_value=settings),patch.object(players_api.frappe,'db',db),patch.object(players_api.frappe,'get_doc',side_effect=[player,enrollment]),self.assertRaises(frappe.ValidationError):
   players_api.register_player.__wrapped__({'full_name':'Name','contact_email':'player@example.invalid'},{},str(uuid4()))
  self.assertIs(db.after_commit,original)
  original.run();earlier.assert_called_once();orphan.assert_not_called()
  db.rollback.assert_called_once_with(save_point='sports_registration')


 def test_provisioning_role_inference_guard_is_scoped_even_on_failure(self):
  import sys
  module=SimpleNamespace(parse_full_name=lambda name:('Player','',''))
  for initial in (None, False, True):
   flags=frappe._dict(setting_role=initial)
   user=SimpleNamespace(flags=frappe._dict())
   def insert(**kwargs):
    self.assertTrue(flags.setting_role)
    self.assertEqual(kwargs,{'ignore_permissions':True})
    raise frappe.ValidationError('Provisioning rejected')
   user.insert=insert
   with self.subTest(initial=initial),patch.dict(sys.modules,{'erpnext.selling.doctype.customer.customer':module}),patch.object(players,'require_player_access'),patch.object(players.frappe,'flags',flags),patch.object(players.frappe,'get_doc',return_value=user),self.assertRaises(frappe.ValidationError):
    players.create_player_user(frappe._dict(full_name='Player',contact_email='player@example.invalid'))
   self.assertIs(flags.setting_role,initial)
