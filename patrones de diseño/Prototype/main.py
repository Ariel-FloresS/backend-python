from concrete_prototype import SystemConfigPrototype

def main():

    original_config = SystemConfigPrototype(configuration = {
                                                'OS':'Linux',
                                                'Version':'Ubuntu 18.04'
                                            }
                    )
    cloned_config = original_config.clone()
    print(f'original {original_config.configuration}')
    print(f' cloned:  {cloned_config.configuration}')

if '__main__'==__name__:

    main()

