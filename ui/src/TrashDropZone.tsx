import { useDroppable } from '@dnd-kit/core'
import {PIcon, PText} from '@porsche-design-system/components-react'

export function TrashDropZone() {
    const { setNodeRef, isOver, active } = useDroppable({
        id: 'trash-zone',
        data: {
            type: 'trash'
        }
    })

    const dropZoneStyle = {
        padding: '24px',
        margin: '24px 16px',
        border: isOver && active ? '3px dashed var(--tf-status-error)' : '2px dashed var(--tf-border)',
        borderRadius: 'var(--tf-radius)',
        backgroundColor: isOver && active ? 'rgba(255, 77, 79, 0.1)' : 'rgba(255, 255, 255, 0.02)',
        display: 'flex',
        flexDirection: 'column' as const,
        alignItems: 'center',
        gap: '8px',
        transition: 'all 200ms ease',
        cursor: isOver && active ? 'pointer' : 'default'
    }

    return (
        <div ref={setNodeRef} style={dropZoneStyle}>
            <PIcon
                name="delete"
                size="medium"
                style={{ color: isOver && active ? 'var(--tf-status-error)' : 'inherit' }}
                theme="dark"
            />
            <PText
                size="small"
                weight="semi-bold"
                style={{ color: isOver && active ? 'var(--tf-status-error)' : 'inherit' }}
                theme="dark"
            >
                {isOver && active ? 'Release to Delete' : 'Drag here to delete'}
            </PText>
        </div>
    )
}
