from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch
from types import SimpleNamespace
import frappe
from sports_app import development_api as api
from sports_app import story_tracking as service


class TestStoryTracking(TestCase):
 def setUp(self):
  folder=TemporaryDirectory();self.addCleanup(folder.cleanup);self.root=Path(folder.name)
  self.path='backlog/user-stories/us-003-01-example.md';self.target=self.root/self.path;self.target.parent.mkdir(parents=True)
  self.target.write_text('# US-003-01: Example\n\n- State: In progress — prototype only\n- Priority: Must\n\n## Acceptance criteria\n\nKeep original evidence.\n- Origin: **Both** — baseline and questionnaire\n')
  (self.root/'backlog/epics').mkdir();self.epic=self.root/'backlog/epics/EPIC-003-test.md'
  self.epic.write_text('| Story | State | Origin | Priority |\n|---|---|---|---|\n| [US-003-01: Example](../user-stories/us-003-01-example.md) | In progress | Both | Must |\n')
  self.overview=self.root/'backlog/README.md';self.overview.write_text('| Story | Current state | Origin |\n|---|---|---|\n| [US-003-01: Example](user-stories/us-003-01-example.md) | In progress | Both |\n\n## Delivery-state snapshot\n\n- In progress: 1\n\n[Consolidation build log](x.md)\n')
  (self.root/'build-logs').mkdir();(self.root/'build-logs/index.md').write_text('| Date | Entry | Status |\n|---|---|---|\n')
  def throw(message,exc=frappe.ValidationError):raise exc(message)
  for target,name,value in ((frappe,'throw',throw),(frappe,'session',SimpleNamespace(user='reviewer@example.test')),(api,'_',lambda s:s),(api,'_root',lambda:self.root),(api,'require_settings_access',lambda:None)):
   active=patch.object(target,name,value);active.start();self.addCleanup(active.stop)
 def meta(self):return service.metadata(self.path,self.target.read_text())
 def update(self,**kwargs):return api.update_story.__wrapped__(self.path,self.meta()['revision'],**kwargs)
 def test_metadata_supports_legacy_status_and_preserves_qualifiers(self):
  self.assertEqual(self.meta()['state'],'In progress — prototype only');self.assertEqual(self.meta()['origin'],'Both')
  self.target.write_text('# US-003-01\n\n- Status: In Review — development slice\n')
  self.assertEqual(self.meta()['state'],'In Review — development slice')
  self.update(priority='Should');self.assertIn('- Status: In Review — development slice',self.target.read_text())
 def test_update_syncs_audit_story_epic_and_master(self):
  data=self.update(state='Done',priority='Should',note='Acceptance evidence reviewed.')
  self.assertEqual(data['state'],'Done');self.assertIn('- Priority: Should',self.target.read_text());self.assertIn('Keep original evidence.',self.target.read_text())
  self.assertIn('| Done | Both | Should |',self.epic.read_text());self.assertIn('| Done | Both |',self.overview.read_text());self.assertIn('- Done: 1',self.overview.read_text())
  audit=(self.root/data['audit_path']).read_text();self.assertIn('reviewer@example.test',audit);self.assertIn('Acceptance evidence reviewed.',audit)
  self.assertIn(Path(data['audit_path']).name,(self.root/'build-logs/index.md').read_text())
 def test_stale_revision_cannot_overwrite(self):
  old=self.meta()['revision'];self.update(priority='Could')
  with self.assertRaises(frappe.ValidationError):api.update_story.__wrapped__(self.path,old,state='Done')
  self.assertNotIn('- State: Done',self.target.read_text())
 def test_invalid_fields_do_not_write(self):
  original=self.target.read_text()
  for kwargs in ({'state':'made up'},{'priority':'High'},{'note':'x'*1001,'state':'Done'},{}):
   with self.subTest(kwargs=str(kwargs)[:50]),self.assertRaises(frappe.ValidationError):self.update(**kwargs)
  self.assertEqual(self.target.read_text(),original)
 def test_denied_role_and_arbitrary_paths(self):
  with patch.object(api,'require_settings_access',side_effect=frappe.PermissionError),self.assertRaises(frappe.PermissionError):self.update(state='Done')
  for path in ('../escape.md','backlog/README.md','build-logs/index.md'):
   with self.subTest(path=path),self.assertRaises(frappe.PermissionError):api.update_story.__wrapped__(path,'x',state='Done')
 def test_unchanged_edit_is_noop(self):
  original=self.target.read_text();self.update(priority='Must');self.assertEqual(self.target.read_text(),original)
  self.assertEqual(len(list((self.root/'build-logs').glob('*.md'))),1)
 def test_failure_restores_all_files_and_removes_partial_audit(self):
  originals={p:p.read_text() for p in self.root.rglob('*.md')};atomic=service._atomic;count=0
  def fail_once(path,content):
   nonlocal count
   count+=1
   if count==3:raise OSError('injected write failure')
   return atomic(path,content)
  with patch.object(service,'_atomic',side_effect=fail_once),self.assertRaises(OSError):self.update(state='Done')
  self.assertEqual({p:p.read_text() for p in self.root.rglob('*.md')},originals)
 def test_symlink_escape_denied(self):
  outside=self.root.parent/(self.root.name+'-outside.md');outside.write_text('Private');self.addCleanup(outside.unlink)
  self.target.unlink();self.target.symlink_to(outside)
  with self.assertRaises(frappe.PermissionError):api.update_story.__wrapped__(self.path,'x',state='Done')
  self.assertEqual(outside.read_text(),'Private')
