import { useDraggable } from '@dnd-kit/core'
import { CSS } from '@dnd-kit/utilities'
import {PButton, PText, PFlex, PIcon} from '@porsche-design-system/components-react'
import { type Keyword } from './api'

interface DraggableKeywordProps {
    keyword: Keyword
    onEdit: (keyword: Keyword) => void
}

export function DraggableKeyword({ keyword, onEdit }: DraggableKeywordProps) {
    const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
        id: keyword.id,
        data: {
            keyword,
            currentType: keyword.type,
            currentSubType: keyword.sub_type,
            currentSubCategory: keyword.sub_category
        }
    })

    const style = {
        transform: CSS.Translate.toString(transform),
        opacity: isDragging ? 0.5 : 1,
        cursor: isDragging ? 'grabbing' : 'grab',
        transition: 'opacity 200ms ease'
    }

    // Show "-" prefix in UI for Exclusion type
    const isExclusion = keyword.type === 'Exclusion'
    const displayWeight = isExclusion && keyword.weight > 0
        ? -keyword.weight
        : keyword.weight

    return (
        <div
            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
            className="keyword-draggable"
        >
            <style>{`
        .keyword-draggable:hover .drag-handle {
          opacity: 0.6 !important;
        }
        .keyword-draggable:active .drag-handle {
          opacity: 1 !important;
        }
        .keyword-panel:hover {
          box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
          border-color: var(--tf-accent) !important;
        }
      `}</style>
            <div
                style={{
                    margin: '6px 12px 6px 60px',
                    padding: '8px 12px',
                    backgroundColor: 'var(--tf-bg-input)',
                    borderRadius: 'var(--tf-radius-sm)',
                    border: '1px solid var(--tf-border)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '12px',
                    position: 'relative',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                    transition: 'all 200ms',
                    maxWidth: 'fit-content'
                }}
                className="keyword-panel"
            >
                <div style={{
                    position: 'absolute',
                    left: '-20px',
                    opacity: 0.3,
                    transition: 'opacity 200ms'
                }} className="drag-handle">
                    <PIcon name="drag" size="small" theme="dark" />
                </div>
                <PText weight="semi-bold" size="small" theme="dark">{keyword.term}</PText>
                <PFlex alignItems="center" style={{ gap: '4px' }}>
                    <PIcon
                        name={displayWeight >= 0 ? 'arrow-head-up' : 'arrow-head-down'}
                        color={displayWeight >= 0 ? 'notification-success' : 'notification-error'}
                        size="x-small"
                        theme="dark"
                    />
                    <PText
                        size="x-small"
                        color={displayWeight >= 0 ? 'notification-success' : 'notification-error'}
                        weight="semi-bold"
                        theme="dark"
                    >
                        {displayWeight > 0 ? '+' : ''}{displayWeight.toFixed(1)}
                    </PText>
                </PFlex>
                <div onClick={(e) => e.stopPropagation()}>
                    <PButton
                        variant="secondary"
                        icon="edit"
                        hideLabel
                        onClick={() => onEdit(keyword)}
                        compact
                        theme="dark"
                    >Edit</PButton>
                </div>
            </div>
        </div>
    )
}
