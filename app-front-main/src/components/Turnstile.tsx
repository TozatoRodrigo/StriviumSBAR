import { Turnstile as TurnstileComponent, TurnstileProps } from '@marsidev/react-turnstile'

export const Turnstile = (props: Omit<TurnstileProps, 'siteKey'>) => (
  <TurnstileComponent
    {...props}
    siteKey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY!}
    options={{ theme: 'light', size: 'flexible', ...props.options }}
  />
)
