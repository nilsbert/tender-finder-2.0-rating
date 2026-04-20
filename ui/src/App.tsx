import { useState, useEffect, useMemo, useRef, type FC, type ReactNode } from 'react'
import AdminHeader from './components/layout/AdminHeader';
import {
  PButton,
  PTextFieldWrapper,
  PSelectWrapper,
  PModal,
  PHeading,
  PText,
  PTag,
  PIcon,
  PFlex,
} from '@porsche-design-system/components-react'
import { DndContext, type DragEndEvent, PointerSensor, KeyboardSensor, useSensor, useSensors, rectIntersection } from '@dnd-kit/core'
import { api, type Keyword, type KeywordCreate } from './api'
import { useURLState } from './useURLState'
import { DraggableKeyword } from './DraggableKeyword'
import { DroppableGroup } from './DroppableGroup'
import { TrashDropZone } from './TrashDropZone'
import { ImportDiffModal, type KeywordImportSummary } from './ImportDiffModal'

// --- Internal Components ---

const StandardPageHeader: FC<{ title: string; subtitle?: string; actions?: ReactNode; children?: ReactNode }> = ({ 
  title, subtitle, actions, children 
}) => (
  <div style={{
    backgroundColor: 'var(--tf-bg-card)',
    padding: '24px',
    borderRadius: 'var(--tf-radius)',
    border: '1px solid var(--tf-border)',
    boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
    marginBottom: '24px'
  }}>
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: children ? '24px' : '0'
    }}>
      <div>
        <PHeading size="large" theme="dark">{title}</PHeading>
        {subtitle && <PText size="small" color="inherit" style={{ opacity: 0.6 }} theme="dark">{subtitle}</PText>}
      </div>
      {actions && <div style={{ display: 'flex', gap: '16px' }}>{actions}</div>}
    </div>
    {children}
  </div>
);

const StandaloneHeader: FC = () => (
  <AdminHeader activeService="rating" />
);

function App() {
  const [keywords, setKeywords] = useState<Keyword[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)

  // Form State
  const [formData, setFormData] = useState<KeywordCreate>({ term: '', weight: 1.0, type: 'Service', sub_type: '', category: 'Uncategorized' })
  const [existingSubTypes, setExistingSubTypes] = useState<string[]>([])

  // Import/Export State
  const [importModalOpen, setImportModalOpen] = useState(false)
  const [importSummary, setImportSummary] = useState<KeywordImportSummary | null>(null)
  const [isImporting, setIsImporting] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Search, Filter, Sort State (URL-synced)
  const [searchQuery, setSearchQuery] = useURLState('search', '')
  const [typeFilter, setTypeFilter] = useURLState('type', '')
  const [subTypeFilter, setSubTypeFilter] = useURLState('subtype', '')
  const [sortBy] = useURLState('sort', 'term')
  const [sortOrder] = useURLState('order', 'asc')

  // Tree expand state
  const [expandedGroups, setExpandedGroups] = useState<Set<string>>(new Set(['Service', 'Sector']))

  const toggleGroup = (groupKey: string) => {
    const newExpanded = new Set(expandedGroups)
    if (newExpanded.has(groupKey)) newExpanded.delete(groupKey)
    else newExpanded.add(groupKey)
    setExpandedGroups(newExpanded)
  }

  const fetchKeywords = async () => {
    try {
      setKeywords(await api.getKeywords())
    } catch (error) {
      console.error('Failed to fetch keywords', error)
    }
  }

  const fetchSubTypes = async () => {
    try {
      setExistingSubTypes(await api.getCategories())
    } catch { /* noop */ }
  }

  useEffect(() => {
    fetchKeywords()
    fetchSubTypes()
  }, [])

  const openAddModal = () => {
    setFormData({ term: '', weight: 1.0, type: 'Service', sub_type: '', category: 'Uncategorized' })
    setEditingId(null)
    setIsModalOpen(true)
  }

  const handleEdit = (k: Keyword) => {
    setFormData({ 
      term: k.term, 
      weight: k.weight, 
      type: k.type || 'Service', 
      sub_type: k.sub_type || '', 
      category: k.category || 'Uncategorized' 
    })
    setEditingId(k.id)
    setIsModalOpen(true)
  }

  const handleDelete = async (id: string) => {
    try {
      await api.deleteKeyword(id)
      await fetchKeywords()
    } catch (error) {
      console.error('Failed to delete keyword', error)
      alert('Failed to delete keyword. Please try again.')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const cleanTerm = formData.term.trim()
    if (!cleanTerm || cleanTerm.length < 2) { alert("Keyword term must be at least 2 characters."); return }
    const duplicate = keywords.find(k => k.term.toLowerCase() === cleanTerm.toLowerCase() && k.id !== editingId)
    if (duplicate) { alert(`Keyword "${cleanTerm}" already exists.`); return }

    const payload = { ...formData, term: cleanTerm }
    try {
      if (editingId) await api.updateKeyword(editingId, payload)
      else await api.createKeyword(payload)
      setIsModalOpen(false)
      fetchKeywords()
      fetchSubTypes()
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || error.message || 'Failed to save keyword'}`)
    }
  }

  // Drag and drop
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 10 } }),
    useSensor(KeyboardSensor)
  )

  const customCollisionDetection = (args: any) => {
    const trashZone = args.droppableContainers.find((c: any) => c.id === 'trash-zone')
    if (trashZone) {
      const collisions = rectIntersection({ ...args, droppableContainers: [trashZone] })
      if (collisions.length > 0) return collisions
    }
    return rectIntersection(args)
  }

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event
    if (!over) return

    const keywordId = active.id as string
    const dropData = over.data.current as { type: string; sub_type: string; sub_category?: string }
    const dragData = active.data.current as { keyword: Keyword; currentType: string; currentSubType: string }

    if (over.id === 'trash-zone' || (over.data.current as any)?.type === 'trash') {
      await handleDelete(keywordId)
      return
    }

    if (dragData.currentType === dropData.type && dragData.currentSubType === dropData.sub_type) return

    const keyword = dragData.keyword
    let newWeight = keyword.weight
    // Automatic weight adjustment based on type switch
    if (dropData.type === 'Exclusion' && newWeight > 0) newWeight = -newWeight
    else if (['Service', 'Sector'].includes(dropData.type) && newWeight < 0) newWeight = -newWeight

    try {
      await api.updateKeyword(keywordId, { 
        term: keyword.term, 
        weight: newWeight, 
        type: dropData.type, 
        sub_type: dropData.sub_type,
        category: keyword.category || 'Uncategorized'
      })
      fetchKeywords()
      fetchSubTypes()
    } catch (error) {
      console.error('Failed to move keyword:', error)
      alert('Failed to move keyword. Please try again.')
    }
  }

  // Group & filter keywords
  const filteredAndSortedKeywords = useMemo(() => {
    let filtered = [...keywords]
    if (searchQuery) filtered = filtered.filter(k => k.term.toLowerCase().includes(searchQuery.toLowerCase()))
    if (typeFilter) filtered = filtered.filter(k => k.type === typeFilter)
    if (subTypeFilter) filtered = filtered.filter(k => k.sub_type === subTypeFilter)

    filtered.sort((a, b) => {
      if (sortBy === 'term') return sortOrder === 'asc' ? a.term.localeCompare(b.term) : b.term.localeCompare(a.term)
      return sortOrder === 'asc' ? a.weight - b.weight : b.weight - a.weight
    })

    const typeMap = new Map<string, { type: string; subtypes: { name: string; keywords: Keyword[] }[] }>()
    filtered.forEach(k => {
      const type = k.type || 'Service'
      const subType = k.sub_type || 'Unassigned'
      if (!typeMap.has(type)) typeMap.set(type, { type, subtypes: [] })
      const typeGroup = typeMap.get(type)!
      let subTypeGroup = typeGroup.subtypes.find(s => s.name === subType)
      if (!subTypeGroup) { subTypeGroup = { name: subType, keywords: [] }; typeGroup.subtypes.push(subTypeGroup) }
      subTypeGroup.keywords.push(k)
    })

    const grouped = Array.from(typeMap.values())
    grouped.sort((a, b) => { 
        if (a.type === 'Exclusion') return 1; 
        if (b.type === 'Exclusion') return -1; 
        return a.type.localeCompare(b.type) 
    })
    grouped.forEach(g => {
      g.subtypes.sort((a, b) => { 
          if (a.name === 'Unassigned') return 1; 
          if (b.name === 'Unassigned') return -1; 
          return a.name.localeCompare(b.name) 
      })
    })
    return grouped
  }, [keywords, searchQuery, typeFilter, subTypeFilter, sortBy, sortOrder])

  const handleExport = () => api.exportKeywords()
  const handleImportClick = () => { if (fileInputRef.current) { fileInputRef.current.value = ''; fileInputRef.current.click() } }

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return
    setIsImporting(true)
    try {
      const result = await api.importKeywords(file, true, false)
      setImportSummary(result.summary)
      setImportModalOpen(true)
    } catch (error: any) {
      alert(`Import analysis failed: ${error.response?.data?.detail || error.message}`)
    } finally {
      setIsImporting(false)
    }
  }

  const handleImportConfirm = async (deleteMissing: boolean) => {
    const file = fileInputRef.current?.files?.[0]
    if (!file) return
    setIsImporting(true)
    try {
      await api.importKeywords(file, false, deleteMissing)
      setImportModalOpen(false)
      setImportSummary(null)
      fetchKeywords()
      alert("Import completed successfully.")
    } catch (error: any) {
      alert(`Import failed: ${error.response?.data?.detail || error.message}`)
    } finally {
      setIsImporting(false)
    }
  }

  const clearFilters = () => {
    setSearchQuery('')
    setTypeFilter('')
    setSubTypeFilter('')
  }

  const totalKeywords = keywords.length

  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'var(--tf-bg-surface)' }}>
      <StandaloneHeader />

      <main style={{ maxWidth: '1400px', margin: '0 auto', padding: '32px 40px' }}>
          <StandardPageHeader
            title="Search Keywords"
            subtitle="Manage keywords and weights for scoring government tenders."
          >
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '24px' }}>
              <PFlex alignItems="flex-end" style={{ gap: '16px', flexWrap: 'wrap' }}>
                <div style={{ flex: 1, minWidth: '200px' }}>
                  <PTextFieldWrapper label="Search keywords" theme="dark">
                    <input
                      type="text"
                      placeholder="Search terms..."
                      value={searchQuery}
                      onChange={e => setSearchQuery(e.target.value)}
                      style={{ width: '100%', height: '40px' }}
                    />
                  </PTextFieldWrapper>
                </div>

                <div style={{ minWidth: '140px' }}>
                  <PSelectWrapper label="Type" theme="dark">
                    <select value={typeFilter} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setTypeFilter(e.target.value)} style={{ height: '40px' }}>
                      <option value="">All Types</option>
                      <option value="Service">Service</option>
                      <option value="Sector">Sector</option>
                      <option value="Exclusion">Exclusion</option>
                    </select>
                  </PSelectWrapper>
                </div>

                <div style={{ minWidth: '180px' }}>
                  <PSelectWrapper label="Sub-type" theme="dark">
                    <select value={subTypeFilter} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSubTypeFilter(e.target.value)} style={{ height: '40px' }}>
                      <option value="">All Sub-types</option>
                      {existingSubTypes.map(cat => (<option key={cat} value={cat}>{cat}</option>))}
                    </select>
                  </PSelectWrapper>
                </div>

                {(searchQuery || typeFilter || subTypeFilter) && (
                  <PButton variant="tertiary" icon="close" onClick={clearFilters} style={{ marginBottom: '2px' }} theme="dark">Clear</PButton>
                )}
              </PFlex>

              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <PButton variant="primary" icon="plus" onClick={openAddModal} theme="dark">Add Keyword</PButton>
                <PFlex>
                  <PButton variant="tertiary" icon="download" onClick={handleExport} theme="dark">Export</PButton>
                  <PButton variant="tertiary" icon="upload" onClick={handleImportClick} loading={isImporting} theme="dark">Import</PButton>
                  <input type="file" ref={fileInputRef} style={{ display: 'none' }} accept="application/json,.json,.JSON,application/x-yaml,.yaml,.yml" onChange={handleFileSelect} />
                </PFlex>
                <div style={{ textAlign: 'right', color: 'var(--tf-text-muted)', flex: 1 }}>
                  <PText size="small" theme="dark">{totalKeywords} keywords defined</PText>
                </div>
              </div>
            </div>
          </StandardPageHeader>

          <DndContext sensors={sensors} onDragEnd={handleDragEnd} collisionDetection={customCollisionDetection}>
            <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {filteredAndSortedKeywords.map(typeGroup => (
                <DroppableGroup
                  key={typeGroup.type}
                  id={`type-${typeGroup.type}`}
                  type={typeGroup.type}
                  isExpanded={expandedGroups.has(typeGroup.type)}
                  onAutoExpand={() => toggleGroup(typeGroup.type)}
                  style={{ backgroundColor: 'var(--tf-bg-card)', borderRadius: 'var(--tf-radius)', border: '1px solid var(--tf-border)', overflow: 'hidden' }}
                >
                  <div
                    style={{ padding: '16px 24px', backgroundColor: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--tf-border)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
                    onClick={() => toggleGroup(typeGroup.type)}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <PIcon name={expandedGroups.has(typeGroup.type) ? 'arrow-head-down' : 'arrow-head-right'} theme="dark" />
                      <PHeading size="small" tag="h3" theme="dark">{typeGroup.type}s</PHeading>
                      <PTag color="background-base" theme="dark">{typeGroup.subtypes.reduce((acc: number, sub: any) => acc + sub.keywords.length, 0)}</PTag>
                    </div>
                  </div>

                  {expandedGroups.has(typeGroup.type) && (
                    <div style={{ paddingBottom: '8px' }}>
                      {typeGroup.subtypes.map(subTypeGroup => (
                        <DroppableGroup
                          key={subTypeGroup.name}
                          id={`subtype-${typeGroup.type}-${subTypeGroup.name}`}
                          type={typeGroup.type}
                          subType={subTypeGroup.name}
                          isExpanded={expandedGroups.has(`${typeGroup.type}-${subTypeGroup.name}`)}
                          onAutoExpand={() => toggleGroup(`${typeGroup.type}-${subTypeGroup.name}`)}
                        >
                          <div
                            style={{ padding: '10px 24px 10px 48px', backgroundColor: 'transparent', borderTop: '1px solid var(--tf-border)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
                            onClick={() => toggleGroup(`${typeGroup.type}-${subTypeGroup.name}`)}
                          >
                            <PIcon name={expandedGroups.has(`${typeGroup.type}-${subTypeGroup.name}`) ? 'arrow-head-down' : 'arrow-head-right'} size="small" theme="dark" />
                            <PText weight="semi-bold" size="small" theme="dark">{subTypeGroup.name}</PText>
                            <PText size="x-small" color="inherit" style={{ opacity: 0.5 }} theme="dark">({subTypeGroup.keywords.length})</PText>
                          </div>

                          {expandedGroups.has(`${typeGroup.type}-${subTypeGroup.name}`) && (
                            <div style={{ padding: '0 48px 8px 64px' }}>
                              {subTypeGroup.keywords.map((k: Keyword) => (
                                <DraggableKeyword key={k.id} keyword={k} onEdit={handleEdit} />
                              ))}
                              {subTypeGroup.keywords.length === 0 && (
                                <PText color="inherit" style={{ opacity: 0.5, padding: '8px' }} size="small" theme="dark">Empty group.</PText>
                              )}
                            </div>
                          )}
                        </DroppableGroup>
                      ))}
                    </div>
                  )}
                </DroppableGroup>
              ))}

              <TrashDropZone />
            </div>
          </DndContext>
      </main>

      <PModal open={isModalOpen} onDismiss={() => setIsModalOpen(false)} heading={editingId ? 'Edit Keyword' : 'New Keyword'} theme="dark">
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '16px 0' }}>
            <PTextFieldWrapper label="Term" theme="dark">
              <input
                autoFocus
                required
                type="text"
                value={formData.term}
                onChange={e => setFormData({ ...formData, term: e.target.value })}
                placeholder="e.g. Cloud, Construction, Security..."
                style={{ width: '100%', padding: '8px' }}
              />
            </PTextFieldWrapper>

            <div>
              <PText weight="semi-bold" style={{ marginBottom: '12px' }} theme="dark">
                Weight / Score Impact: {formData.weight.toFixed(1)}
              </PText>
              <input
                type="range"
                min="-5"
                max="5"
                step="0.5"
                value={formData.weight}
                onChange={e => setFormData({ ...formData, weight: parseFloat(e.target.value) })}
                style={{ width: '100%', accentColor: 'var(--tf-accent)' }}
              />
              <PFlex justifyContent="space-between" style={{ marginTop: '4px' }}>
                <PText size="x-small" color="inherit" style={{ opacity: 0.5 }} theme="dark">Exclusion (-5.0)</PText>
                <PText size="x-small" color="inherit" style={{ opacity: 0.5 }} theme="dark">Neutral (0)</PText>
                <PText size="x-small" color="inherit" style={{ opacity: 0.5 }} theme="dark">Highly Relevant (5.0)</PText>
              </PFlex>
            </div>

            <PFlex justifyContent="flex-end" style={{ gap: '12px' }}>
              <PButton type="button" variant="tertiary" onClick={() => setIsModalOpen(false)} theme="dark">Cancel</PButton>
              <PButton type="submit" theme="dark">{editingId ? 'Save Changes' : 'Add Keyword'}</PButton>
            </PFlex>
          </div>
        </form>
      </PModal>

      <ImportDiffModal
        isOpen={importModalOpen}
        onClose={() => setImportModalOpen(false)}
        summary={importSummary}
        onConfirm={handleImportConfirm}
        isExecuting={isImporting}
      />
    </div>
  )
}

export default App