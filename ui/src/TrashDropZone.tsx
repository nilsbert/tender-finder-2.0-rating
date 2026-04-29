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
        border: isOver && active ? '3px dashed var(--pds-notification-error)' : '2px dashed var(--tf-border)',
        borderRadius: 'var(--tf-radius)',
        backgroundColor: isOver && active ? 'rgba(255, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.02)',
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
                color={isOver && active ? 'notification-error' : 'contrast-low'}
                theme="dark"
            />
            <PText
                size="small"
                weight="semi-bold"
                color={isOver && active ? 'notification-error' : 'contrast-low'}
                theme="dark"
            >
                {isOver && active ? 'Release to Delete' : 'Drag here to delete'}
            </PText>
        </div>
    )
}
