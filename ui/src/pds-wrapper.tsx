// @ts-nocheck
import React from 'react';
// Import needed components from the real package bypassing exports map
// @ts-ignore
import * as PDS from '../node_modules/@porsche-design-system/components-react/esm/public-api.mjs';

// Export everything
export * from '../node_modules/@porsche-design-system/components-react/esm/public-api.mjs';

// Alias PHeading to PHeadline if needed
export const PHeading = PDS.PHeading || PDS.PHeadline;
export const PHeadline = PDS.PHeadline || PDS.PHeading;
export const PText = PDS.PText;
export const PTag = PDS.PTag;
export const PIcon = PDS.PIcon;
export const PButton = PDS.PButton;
export const PModal = PDS.PModal;

const { 
  PInputText, 
  PSelect: PDSSelect, 
  PSelectOption, 
  PCheckbox: PDSCheckbox, 
  PTextarea: PDSTextarea 
} = PDS;

// Polyfill removed components
export const PContentWrapper = ({ children, style }: any) => {
  return <div className="p-content-wrapper" style={style}>{children}</div>;
};

export const PFlex = ({ children, direction, gap, alignItems, justifyContent, style }: any) => {
  const flexStyle = {
    display: 'flex',
    flexDirection: direction || 'row',
    gap: gap || '0px',
    alignItems: alignItems || 'stretch',
    justifyContent: justifyContent || 'flex-start',
    ...style
  };
  return <div style={flexStyle}>{children}</div>;
};

export const PFlexItem = ({ children, grow, shrink, style }: any) => {
  const itemStyle = {
    flexGrow: grow || 0,
    flexShrink: shrink || 1,
    ...style
  };
  return <div style={itemStyle}>{children}</div>;
};

export const PGrid = ({ children, style }: any) => {
  return <div style={{ display: 'grid', ...style }}>{children}</div>;
};

export const PGridItem = ({ children, style }: any) => {
  return <div style={style}>{children}</div>;
};

export const PTextFieldWrapper = ({ label, children, hideLabel, description }: any) => {
  if (!children) return null;
  const child = React.Children.only(children) as React.ReactElement;
  const props = child.props as any;
  const { value, onChange, placeholder, disabled, name, type } = props;
  
  return (
    <PInputText
      label={hideLabel ? '' : label}
      value={value}
      onInput={(e: any) => onChange && onChange({ target: { value: e.target.value, name } })}
      placeholder={placeholder}
      disabled={disabled}
      name={name}
      type={type || 'text'}
      description={description}
    />
  );
};

export const PSelectWrapper = ({ label, children, hideLabel, description }: any) => {
  if (!children) return null;
  const child = React.Children.only(children) as React.ReactElement;
  const props = child.props as any;
  const { value, onChange, name } = props;
  const options = React.Children.toArray(props.children);

  return (
    <PDSSelect
      label={hideLabel ? '' : label}
      value={value}
      onChange={(e: any) => onChange && onChange({ target: { value: e.target.value, name } })}
      name={name}
      description={description}
    >
      {options.map((opt: any, idx) => {
        if (!opt || !opt.props) return null;
        return (
          <PSelectOption key={idx} value={opt.props.value}>
            {opt.props.children}
          </PSelectOption>
        );
      })}
    </PDSSelect>
  );
};

export const PCheckboxWrapper = ({ label, children, hideLabel }: any) => {
  if (!children) return null;
  const child = React.Children.only(children) as React.ReactElement;
  const props = child.props as any;
  const { checked, onChange, name } = props;

  return (
    <PDSCheckbox
      label={hideLabel ? '' : label}
      checked={checked}
      onChange={(e: any) => onChange && onChange({ target: { checked: e.target.checked, name } })}
      name={name}
    />
  );
};

export const PTextareaWrapper = ({ label, children, description }: any) => {
  if (!children) return null;
  const child = React.Children.only(children) as React.ReactElement;
  const props = child.props as any;
  const { value, onChange, placeholder, disabled, name } = props;

  return (
    <PDSTextarea
      label={label}
      value={value}
      onInput={(e: any) => onChange && onChange({ target: { value: e.target.value, name } })}
      placeholder={placeholder}
      disabled={disabled}
      name={name}
      description={description}
    />
  );
};
